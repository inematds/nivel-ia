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
import argparse, collections, json, os, re, subprocess, sys
from datetime import datetime, timedelta, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
REG = os.path.join(AQUI, '..', 'registro')
HOME = os.path.expanduser('~')
RODADAS = os.path.join(HOME, '.local/share/inema/rodadas.jsonl')
YTPUBX = os.path.join(HOME, '.local/share/yt-pubx/historico.jsonl')
VIGIA_POR_DIA = 24  # roda mais de 24 vezes por dia = vigia (cuida da casa), não motor de entrega
MINUTOS_PADRAO = {'_leia': 'Minutos que cada coisa custaria à mão. Estimativa: ajuste os números à sua realidade.',
                  'video_publicado': 30, 'rodada_motor_ok': 10, 'vigia_dia': 2}


def timers():
    r = subprocess.run(['systemctl', '--user', 'list-timers', '--all', '--no-legend', '--no-pager'],
                       capture_output=True, text=True, timeout=30)
    nomes = set()
    for linha in r.stdout.splitlines():
        for campo in linha.split():
            if campo.endswith('.timer'):
                nomes.add(campo[:-6])
    return nomes


def execucoes(dias, nomes):
    """{servico: {'ok': n, 'falhou': n, 'ultima_falha': ts}} a partir dos jobs de start do journal."""
    r = subprocess.Popen(['journalctl', '--user', '--since', f'{dias} days ago', '-o', 'json', 'JOB_TYPE=start'],
                         stdout=subprocess.PIPE, text=True)
    out = collections.defaultdict(lambda: {'ok': 0, 'falhou': 0, 'ultima_falha': None})
    alvo = {n + '.service' for n in nomes}
    for linha in r.stdout:
        try:
            d = json.loads(linha)
        except ValueError:
            continue
        u, res = d.get('USER_UNIT'), d.get('JOB_RESULT')
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
    nomes = timers()
    ex = execucoes(dias, nomes)
    motores, vigias = [], []
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
                timers=len(nomes), motores=motores, vigias=vigias,
                rodadas_total=total, falhas_total=falhas,
                acerto=round(100 * (total - falhas) / total, 1) if total else None,
                acerto_motores=round(100 * ok_motores / max(1, sum(x['rodadas'] for x in motores)), 1) if motores else None,
                publicados=len(pub), publicados_por_canal=dict(por_canal.most_common()),
                publicados_por_semana=round(len(pub) / (dias / 7), 1),
                placar=dict(placar), horas_devolvidas=round(horas), minutos=m)


def resumo(r):
    L = [f"Trabalho automático — últimos {r['dias']} dias",
         f"- {len(r['motores'])} motores de entrega e {len(r['vigias'])} vigias ({r['timers']} timers)",
         f"- motores: {sum(m['rodadas'] for m in r['motores'])} execuções, {sum(m['falhou'] for m in r['motores'])} falhas = {r['acerto_motores']}% sem erro (vigias à parte: {sum(v['rodadas'] for v in r['vigias'])} execuções)",
         f"- {r['publicados']} vídeos publicados no YouTube ({r['publicados_por_semana']} por semana)",
         f"- ≈ {r['horas_devolvidas']} h devolvidas (estimativa: registro/motores-minutos.json)"]
    pior = sorted([m for m in r['motores'] if m['falhou']], key=lambda m: -m['falhou'])[:5]
    if pior:
        L.append('- mais falhas: ' + ', '.join(f"{m['nome']} {m['falhou']}/{m['rodadas']}" for m in pior))
    return '\n'.join(L)


def main():
    ap = argparse.ArgumentParser(description='Mede os motores automáticos (sem IA conversando)')
    ap.add_argument('--dias', type=int, default=30)
    ap.add_argument('--registro', default=None)
    a = ap.parse_args()
    global REG
    REG = a.registro or REG
    r = medir(a.dias)
    os.makedirs(REG, exist_ok=True)
    json.dump(r, open(os.path.join(REG, 'motores.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(resumo(r))


if __name__ == '__main__':
    sys.exit(main())
