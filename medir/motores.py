#!/usr/bin/env python3
"""motores.py: mede o trabalho AUTOMÁTICO (motores, robôs, RPA) ao lado da escada de IA.

A escada AL1–AL5 mede a IA conversando com você. Aqui entra o que roda sem conversa nenhuma:
timers do systemd, motores de publicação, vigias. Só leitura, só biblioteca padrão.

Fontes (as que existirem na máquina):
  - journal do systemd de usuário: cada execução de serviço disparado por timer (deu certo / falhou)
  - ~/.local/share/inema/rodadas.jsonl (placar de entregas dos motores, se houver)
  - ~/.local/share/yt-pubx/historico.jsonl (vídeos publicados no YouTube, se houver)
  - registro/motores-minutos.json: quantos minutos cada entrega custaria à mão (você ajusta)

Uso:
  python3 medir/motores.py [--dias 30]        grava registro/motores.json e imprime o resumo
"""
import argparse, collections, json, os, re, socket, subprocess, sys
from datetime import datetime, timedelta, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(AQUI, '..', 'registro')
HOME = os.path.expanduser('~')
RODADAS = os.path.join(HOME, '.local/share/inema/rodadas.jsonl')
YTPUBX = os.path.join(HOME, '.local/share/yt-pubx/historico.jsonl')
VIGIA_POR_DIA = 24  # roda mais de 24 vezes por dia = vigia (cuida da casa), não motor de entrega
MINUTOS_PADRAO = {'_leia': 'Minutos que cada coisa custaria à mão. Estimativa: ajuste os números à sua realidade.',
                  'video_publicado': 30, 'rodada_motor_ok': 10, 'vigia_dia': 2}


# timers que vêm com o sistema (Ubuntu/Debian): manutenção da máquina, não trabalho seu
DISTRO = {'apt-daily', 'apt-daily-upgrade', 'dpkg-db-backup', 'logrotate', 'man-db', 'motd-news', 'e2scrub_all',
          'fstrim', 'systemd-tmpfiles-clean', 'update-notifier-download', 'update-notifier-motd', 'apport-autoreport',
          'snapd.snap-repair', 'ua-timer', 'sysstat-collect', 'sysstat-summary', 'sysstat-rotate', 'xfs_scrub_all',
          'fwupd-refresh', 'certbot', 'launchpadlib-cache-clean', 'anacron', 'phpsessionclean', 'plocate-updatedb',
          'mlocate', 'atop-rotate', 'rasdaemon', 'pamac-cleancache', 'shadow', 'logwatch'}


def _sc(escopo):
    return ['--user'] if escopo == 'user' else []


def timers(escopo='user'):
    r = subprocess.run(['systemctl', *_sc(escopo), 'list-timers', '--all', '--no-legend', '--no-pager'],
                       capture_output=True, text=True, timeout=30)
    nomes = set()
    for linha in r.stdout.splitlines():
        for campo in linha.split():
            if campo.endswith('.timer') and campo[:-6] not in DISTRO:
                nomes.add(campo[:-6])
    return nomes


def execucoes(dias, nomes, escopo='user'):
    """{servico: {'ok': n, 'falhou': n, 'ultima_falha': ts}} a partir dos jobs de start do journal."""
    out = collections.defaultdict(lambda: {'ok': 0, 'falhou': 0, 'ultima_falha': None})
    if not nomes:
        return out
    r = subprocess.Popen(['journalctl', *_sc(escopo), '--since', f'{dias} days ago', '-o', 'json', 'JOB_TYPE=start'],
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    alvo = {n + '.service' for n in nomes}
    campo = 'USER_UNIT' if escopo == 'user' else 'UNIT'
    for linha in r.stdout:
        try:
            d = json.loads(linha)
        except ValueError:
            continue
        u, res = d.get(campo), d.get('JOB_RESULT')
        if u not in alvo or res not in ('done', 'failed'):
            continue
        s = out[u[:-8]]
        if res == 'done':
            s['ok'] += 1
        else:
            s['falhou'] += 1
            s['ultima_falha'] = int(d.get('__REALTIME_TIMESTAMP', 0)) // 1_000_000
    r.wait()
    return out


def cron(dias):
    """linhas ativas do crontab do usuário e quantas vezes o cron rodou comandos no período."""
    r = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    linhas = [l for l in r.stdout.splitlines() if l.strip() and not l.lstrip().startswith('#') and not re.match(r'^\w+=', l)]
    if not linhas:
        return dict(tarefas=0, rodadas=0)
    j = subprocess.run(['journalctl', '--since', f'{dias} days ago', '-t', 'CRON', '-o', 'cat', '--no-pager'],
                       capture_output=True, text=True, timeout=120)
    return dict(tarefas=len(linhas), rodadas=sum(1 for l in j.stdout.splitlines() if ' CMD (' in l))


def ligados():
    """serviços sempre ligados que são seus: containers Docker, processos do pm2 e units próprias ativas."""
    def rodar(cmd):
        try:
            return subprocess.run(cmd, capture_output=True, text=True, timeout=30).stdout
        except (OSError, subprocess.TimeoutExpired):
            return ''
    docker = [l for l in rodar(['docker', 'ps', '--format', '{{.Names}}']).splitlines() if l.strip()]
    pm2 = []
    try:
        pm2 = [p.get('name') for p in json.loads(rodar(['pm2', 'jlist']) or '[]') if (p.get('pm2_env') or {}).get('status') == 'online']
    except ValueError:
        pass
    units = []
    for escopo, pasta in (('sistema', '/etc/systemd/system'), ('user', os.path.join(HOME, '.config/systemd/user'))):
        if not os.path.isdir(pasta):
            continue
        proprias = {f[:-8] for f in os.listdir(pasta) if f.endswith('.service') and not os.path.islink(os.path.join(pasta, f))}
        ativos = rodar(['systemctl', *_sc(escopo), 'list-units', '--type=service', '--state=running', '--no-legend', '--plain', '--no-pager'])
        for l in ativos.splitlines():
            nome = l.split()[0][:-8] if l.split() else ''
            base = nome.split('@')[0] + ('@' if '@' in nome else '')
            if nome in proprias or base in proprias:
                units.append(nome)
    return dict(docker=sorted(docker), pm2=sorted(pm2), units=sorted(units), total=len(docker) + len(pm2) + len(units))


def jsonl(caminho):
    if not os.path.exists(caminho):
        return []
    saida = []
    for linha in open(caminho, encoding='utf-8'):
        try:
            saida.append(json.loads(linha))
        except ValueError:
            pass
    return saida


def quando(d):
    v = d.get('ts') or d.get('data')
    try:
        t = datetime.fromisoformat(v)
        return t if t.tzinfo else t.replace(tzinfo=timezone(timedelta(hours=-3)))
    except (TypeError, ValueError):
        return None


def minutos():
    p = os.path.join(REG, 'motores-minutos.json')
    if not os.path.exists(p):
        os.makedirs(REG, exist_ok=True)
        json.dump(MINUTOS_PADRAO, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return {**MINUTOS_PADRAO, **json.load(open(p, encoding='utf-8'))}


def medir(dias=30):
    lim = datetime.now(timezone.utc) - timedelta(days=dias)
    ex, nomes = {}, set()
    for escopo in ('user', 'sistema'):
        n = timers(escopo)
        nomes |= n
        ex.update(execucoes(dias, n, escopo))
    motores, vigias = [], []
    for nome in sorted(nomes - set(ex)):
        ex[nome] = {'ok': 0, 'falhou': 0, 'ultima_falha': None}  # timer sem execução no período
    for nome, s in sorted(ex.items()):
        total = s['ok'] + s['falhou']
        linha = dict(nome=nome, rodadas=total, ok=s['ok'], falhou=s['falhou'],
                     acerto=round(100 * s['ok'] / total, 1) if total else None, ultima_falha=s['ultima_falha'])
        (vigias if total / dias > VIGIA_POR_DIA else motores).append(linha)
    # entregas: placar dos motores + publicações no YouTube
    rod = [r for r in jsonl(RODADAS) if r.get('fase') == 'fim' and (quando(r) or lim) >= lim]
    placar = collections.Counter(r.get('resultado') or 'sem resultado' for r in rod)
    pub = [p for p in jsonl(YTPUBX) if (quando(p) or lim) >= lim and p.get('video_id')
           and (p.get('privacy') or {}).get('privacyStatus') != 'private']  # privado não é entrega
    por_canal = collections.Counter(p.get('canal') or '?' for p in pub)
    m = minutos()
    ok_motores = sum(x['ok'] for x in motores)
    horas = (len(pub) * m['video_publicado'] + ok_motores * m['rodada_motor_ok'] + len(vigias) * dias * m['vigia_dia']) / 60
    falhas = sum(x['falhou'] for x in motores + vigias)
    total = sum(x['rodadas'] for x in motores + vigias)
    return dict(gerado_em=datetime.now().astimezone().isoformat(timespec='seconds'), dias=dias,
                maquina=socket.gethostname(), cron=cron(dias), ligados=ligados(),
                timers=len(nomes), motores=motores, vigias=vigias,
                rodadas_total=total, falhas_total=falhas,
                acerto=round(100 * (total - falhas) / total, 1) if total else None,
                acerto_motores=round(100 * ok_motores / max(1, sum(x['rodadas'] for x in motores)), 1) if motores else None,
                publicados=len(pub), publicados_por_canal=dict(por_canal.most_common()),
                publicados_por_semana=round(len(pub) / (dias / 7), 1),
                placar=dict(placar), horas_devolvidas=round(horas), minutos=m)


def resumo(r):
    L = [f"Trabalho automático — últimos {r['dias']} dias",
         f"- {len(r['motores'])} motores de entrega e {len(r['vigias'])} vigias ({r['timers']} timers) · {r['ligados']['total']} serviços sempre ligados · cron: {r['cron']['tarefas']} tarefas, {r['cron']['rodadas']} execuções",
         f"- motores: {sum(m['rodadas'] for m in r['motores'])} execuções, {sum(m['falhou'] for m in r['motores'])} falhas = {r['acerto_motores']}% sem erro (vigias à parte: {sum(v['rodadas'] for v in r['vigias'])} execuções)",
         f"- {r['publicados']} vídeos publicados no YouTube ({r['publicados_por_semana']} por semana)",
         f"- ≈ {r['horas_devolvidas']} h devolvidas (estimativa: registro/motores-minutos.json)"]
    pior = sorted([m for m in r['motores'] if m['falhou']], key=lambda m: -m['falhou'])[:5]
    if pior:
        L.append('- mais falhas: ' + ', '.join(f"{m['nome']} {m['falhou']}/{m['rodadas']}" for m in pior))
    return '\n'.join(L)


def juntar(alvo, chave=None):
    """mede outra máquina por SSH (roda este arquivo lá pelo stdin, só leitura) e guarda em registro/motores-maquinas/."""
    cmd = ['ssh', '-o', 'BatchMode=yes', '-o', 'ConnectTimeout=15'] + (['-i', chave] if chave else []) + [alvo, 'python3 - --json']
    r = subprocess.run(cmd, input=open(os.path.abspath(__file__), encoding='utf-8').read(), capture_output=True, text=True, timeout=900)
    if r.returncode:
        raise SystemExit(f'{alvo}: falhou ({r.stderr.strip()[-300:]})')
    dados = json.loads(r.stdout)
    pasta = os.path.join(REG, 'motores-maquinas')
    os.makedirs(pasta, exist_ok=True)
    json.dump(dados, open(os.path.join(pasta, dados['maquina'] + '.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return dados


def geral():
    """soma esta máquina (registro/motores.json) com as juntadas: registro/motores-geral.json."""
    maqs = [json.load(open(os.path.join(REG, 'motores.json'), encoding='utf-8'))]
    pasta = os.path.join(REG, 'motores-maquinas')
    if os.path.isdir(pasta):
        maqs += [json.load(open(os.path.join(pasta, f), encoding='utf-8')) for f in sorted(os.listdir(pasta)) if f.endswith('.json')
                 and f[:-5] != maqs[0]['maquina']]
    m = minutos()
    soma = lambda f: sum(f(x) for x in maqs)
    motores = [dict(x, nome=f"{x['nome']} ({q['maquina']})" if q is not maqs[0] else x['nome']) for q in maqs for x in q['motores']]
    vigias = [dict(x, nome=f"{x['nome']} ({q['maquina']})" if q is not maqs[0] else x['nome']) for q in maqs for x in q['vigias']]
    exec_m = sum(x['rodadas'] for x in motores)
    ok_m = sum(x['ok'] for x in motores)
    pub = collections.Counter()
    for q in maqs:
        pub.update(q['publicados_por_canal'])
    dias = maqs[0]['dias']
    cron_rod = soma(lambda q: q['cron']['rodadas'])
    horas = (sum(pub.values()) * m['video_publicado'] + ok_m * m['rodada_motor_ok'] + len(vigias) * dias * m['vigia_dia']) / 60
    g = dict(gerado_em=datetime.now().astimezone().isoformat(timespec='seconds'), dias=dias, geral=True,
             maquina=f'{len(maqs)} máquinas', maquinas=[dict(maquina=q['maquina'], motores=len(q['motores']), vigias=len(q['vigias']),
             execucoes=sum(x['rodadas'] for x in q['motores']), falhas=sum(x['falhou'] for x in q['motores']),
             ligados=q['ligados']['total'], cron=q['cron'], publicados=q['publicados']) for q in maqs],
             timers=soma(lambda q: q['timers']), motores=motores, vigias=vigias,
             cron=dict(tarefas=soma(lambda q: q['cron']['tarefas']), rodadas=cron_rod),
             ligados=dict(total=soma(lambda q: q['ligados']['total'])),
             rodadas_total=sum(x['rodadas'] for x in motores + vigias), falhas_total=sum(x['falhou'] for x in motores + vigias),
             acerto=None, acerto_motores=round(100 * ok_m / max(1, exec_m), 1),
             publicados=sum(pub.values()), publicados_por_canal=dict(pub.most_common()),
             publicados_por_semana=round(sum(pub.values()) / (dias / 7), 1), placar={}, horas_devolvidas=round(horas), minutos=m)
    json.dump(g, open(os.path.join(REG, 'motores-geral.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return g


def main():
    ap = argparse.ArgumentParser(description='Mede os motores automáticos (sem IA conversando)')
    ap.add_argument('--dias', type=int, default=30)
    ap.add_argument('--registro', default=None)
    ap.add_argument('--json', action='store_true', help='só imprime o JSON (usado pelo juntar, na outra máquina)')
    ap.add_argument('--juntar', nargs='*', metavar='usuario@host', help='mede essas máquinas por SSH e guarda em registro/motores-maquinas/')
    ap.add_argument('--chave', help='chave SSH para o --juntar (uma por vez)')
    ap.add_argument('--geral', action='store_true', help='soma esta máquina com as juntadas em registro/motores-geral.json')
    a = ap.parse_args()
    global REG
    REG = a.registro or REG
    if a.json:
        global minutos
        minutos = lambda: dict(MINUTOS_PADRAO)  # na outra máquina não grava nada
        print(json.dumps(medir(a.dias), ensure_ascii=False))
        return 0
    if a.juntar:
        for alvo in a.juntar:
            d = juntar(alvo, a.chave)
            print(f"{d['maquina']}: {len(d['motores'])} motores, {d['ligados']['total']} serviços ligados, cron {d['cron']['tarefas']} tarefas")
        return 0
    if a.geral:
        g = geral()
        print(resumo(g))
        print('máquinas: ' + ', '.join(f"{q['maquina']} ({q['motores']} motores, {q['ligados']} ligados)" for q in g['maquinas']))
        return 0
    r = medir(a.dias)
    os.makedirs(REG, exist_ok=True)
    json.dump(r, open(os.path.join(REG, 'motores.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(resumo(r))


if __name__ == '__main__':
    sys.exit(main())
