#!/usr/bin/env python3
"""Testes do nivel-ia com logs falsos (nada da sua máquina). Uso: python3 tests/run.py"""
import json
import os
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / 'medir'))
import nivel as N  # noqa: E402

OK = []


def caso(f):
    OK.append(f)
    return f


def claude_log(pasta, nome, humanos, acoes, cmds=(), mcp=(), t0='2026-11-10T10:00:00Z'):
    linhas = [{'type': 'session-owner'}]
    base = N.epoch(t0)
    k = 0
    for h in range(humanos):
        linhas.append({'type': 'user', 'timestamp': ts(base + k * 60), 'cwd': '/p', 'message': {'content': f'pedido {h} sobre vídeo'}}); k += 1
    blocos = [{'type': 'tool_use', 'name': 'Bash', 'input': {'command': c}} for c in cmds]
    blocos += [{'type': 'tool_use', 'name': m, 'input': {}} for m in mcp]
    blocos += [{'type': 'tool_use', 'name': 'Read', 'input': {}} for _ in range(acoes - len(blocos))]
    for b in blocos:
        linhas.append({'type': 'assistant', 'timestamp': ts(base + k * 60), 'message': {'content': [b]}}); k += 1
    arq = Path(pasta) / 'proj' / f'{nome}.jsonl'
    arq.parent.mkdir(parents=True, exist_ok=True)
    arq.write_text('\n'.join(json.dumps(l) for l in linhas) + '\n')
    return arq


def ts(e):
    from datetime import datetime, timezone
    return datetime.fromtimestamp(e, timezone.utc).isoformat().replace('+00:00', 'Z')


def sess(humanos, acoes, automatica=False, minutos=10):
    s = dict(fonte='claude', humanos=humanos, acoes=acoes, automatica=automatica or humanos <= 1, minutos=minutos,
             primeiro='pedido sobre vídeo', inicio=N.epoch('2026-11-10T10:00:00Z'), externo=0, conexoes={'programa:git': 1})
    s['nivel'] = N.nivel(s)
    return s


@caso
def t_al5_sem_conversa():
    assert sess(1, 40)['nivel'] == 'AL5'


@caso
def t_al4_muitas_acoes():
    assert sess(2, 30)['nivel'] == 'AL4'


@caso
def t_al3_meio():
    assert sess(4, 20)['nivel'] == 'AL3'


@caso
def t_al2_pouca_acao():
    assert sess(5, 3)['nivel'] == 'AL2'


@caso
def t_nunca_al1_nos_logs():
    assert all(sess(h, a)['nivel'] != 'AL1' for h in range(0, 8) for a in range(0, 80, 7))


@caso
def t_le_log_claude():
    with tempfile.TemporaryDirectory() as d:
        s = N.ler_claude(str(claude_log(d, 'a', 3, 50, cmds=['git push origin main', 'ffmpeg -i a b'])))
        assert s['humanos'] == 3 and s['acoes'] == 50 and s['nivel'] == 'AL4'
        assert s['externo'] == 1, s['externo']
        assert 'programa:git' in s['conexoes'] and 'programa:ffmpeg' in s['conexoes']


@caso
def t_conexao_mcp_e_externo():
    with tempfile.TemporaryDirectory() as d:
        s = N.ler_claude(str(claude_log(d, 'b', 2, 4, mcp=['mcp__metricool__createScheduledPost', 'mcp__metricool__getBrandSettings'])))
        assert s['conexoes'].get('serviço:metricool') == 2 and s['externo'] == 1


@caso
def t_heredoc_nao_vira_programa():
    c = N.cabeca("python3 - <<'EOF'\nimport json\nfrom x import y\ndef f(): pass\nEOF\nffmpeg -y")
    assert 'programa:import' not in c and 'programa:def' not in c and 'programa:ffmpeg' in c, c


@caso
def t_site_registrado():
    assert 'site:api.exemplo.com' in N.cabeca('curl -s https://api.exemplo.com/v1')


@caso
def t_segredo_oculto():
    t = N.limpa('minha chave sk-abcdefghijklmnop123 e email fulano@x.com')
    assert 'sk-abc' not in t and 'fulano@' not in t


@caso
def t_le_codex():
    with tempfile.TemporaryDirectory() as d:
        arq = Path(d) / 'r.jsonl'
        L = [{'type': 'session_meta', 'payload': {'cwd': '/p', 'originator': 'codex_exec'}},
             {'type': 'response_item', 'timestamp': '2026-11-10T10:00:00Z', 'payload': {'type': 'message', 'role': 'user', 'content': [{'text': 'traduz isso'}]}},
             {'type': 'response_item', 'timestamp': '2026-11-10T10:01:00Z', 'payload': {'type': 'custom_tool_call', 'name': 'exec', 'input': 'await tools.exec_command({cmd:"yt-pubx publicar a.mp4"})'}},
             {'type': 'response_item', 'timestamp': '2026-11-10T10:02:00Z', 'payload': {'type': 'function_call', 'name': 'wait', 'arguments': '{}'}}]
        arq.write_text('\n'.join(json.dumps(l) for l in L))
        s = N.ler_codex(str(arq))
        assert s['nivel'] == 'AL5' and s['acoes'] == 1 and s['externo'] == 1 and 'programa:yt-pubx' in s['conexoes'], s


@caso
def t_papel_valida():
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / 'papel.csv'
        p.write_text('data;tarefa;nivel;minutos;conexao;corrigi\n2026-11-10;Reunião;1;60,5;;n\n2026-11-10;X;AL7;5;;n\n2026-11-10;Y;AL3;0;;n\n', encoding='utf-8')
        linhas, erros = N.ler_papel(p)
        assert len(linhas) == 1 and linhas[0]['nivel'] == 'AL1' and linhas[0]['minutos'] == 60.5 and len(erros) == 2, (linhas, erros)


@caso
def t_papel_modelo_do_kit_valido():
    linhas, erros = N.ler_papel(RAIZ / 'kit' / 'papel-modelo.csv')
    assert len(linhas) == 5 and not erros and {l['nivel'] for l in linhas} == set(N.NIVEIS)


@caso
def t_parte_ia_e_al1_do_papel():
    papel = [dict(data='', tarefa='Reunião', nivel='AL1', minutos=30, conexao='', corrigi=False)]
    r = N.montar([sess(1, 10, minutos=30), sess(5, 3, minutos=40)], papel, N.TAREFAS_PADRAO, 7)
    assert r['escada']['AL1'] == 30.0 and r['escada']['AL5'] == 30.0 and r['parte_ia'] == 30.0, r['escada']


@caso
def t_soma_100():
    r = N.montar([sess(1, 10), sess(2, 40), sess(4, 20), sess(5, 2)], [], N.TAREFAS_PADRAO, 30)
    assert abs(sum(r['escada'].values()) - 100) < 0.5


@caso
def t_critica_para_no_al4():
    s = sess(2, 40); s['primeiro'] = 'publica no telegram'
    r = N.montar([s], [], N.TAREFAS_PADRAO, 7)
    t = r['tarefas'][0]
    assert t['critica'] and t['nivel'] == 'AL4' and t['proximo'] is None


@caso
def t_proximo_degrau_um_por_vez():
    r = N.montar([sess(5, 3)], [], N.TAREFAS_PADRAO, 7)
    assert r['tarefas'][0]['nivel'] == 'AL2' and r['tarefas'][0]['proximo'] == 'AL3'


@caso
def t_conexoes_primeira_ultima():
    a = sess(1, 3); b = sess(1, 3); b['inicio'] += 86400 * 3
    c = N.registro_conexoes([a, b])[0]
    assert c['sessoes'] == 2 and c['primeira'] < c['ultima'] and c['sozinha'] == 2


@caso
def t_markdown_tem_escada_e_subir():
    r = N.montar([sess(5, 3) for _ in range(6)], [], N.TAREFAS_PADRAO, 7)
    md = N.markdown(r, None)
    assert all(n in md for n in N.NIVEIS) and 'Quem pode subir' in md and 'AL0' not in md


@caso
def t_varrer_e_relatorio_ponta_a_ponta():
    with tempfile.TemporaryDirectory() as d:
        claude_log(d, 'x', 1, 20); claude_log(d, 'y', 4, 8)
        reg = Path(d) / 'reg'
        os.utime(Path(d) / 'proj' / 'x.jsonl'); os.utime(Path(d) / 'proj' / 'y.jsonl')
        assert N.main(['--registro', str(reg), 'varrer', '--dias', '36500', '--claude', d, '--codex', str(Path(d) / 'vazio')]) == 0
        assert N.main(['--registro', str(reg), 'relatorio']) == 0
        r = json.loads((reg / 'relatorio.json').read_text())
        assert r['fontes']['claude'] == 2 and (reg / 'relatorio.md').exists() and (reg / 'historico.jsonl').exists()


@caso
def t_registro_fora_do_git():
    gi = (RAIZ / '.gitignore').read_text()
    assert 'registro/*' in gi and '!registro/.gitkeep' in gi


def main():
    falhas = 0
    for f in OK:
        try:
            f(); print('ok  ', f.__name__)
        except Exception as e:  # noqa: BLE001
            falhas += 1; print('FALHA', f.__name__, '→', repr(e))
    print(f'\n{len(OK) - falhas}/{len(OK)} testes passaram')
    return 1 if falhas else 0


if __name__ == '__main__':
    sys.exit(main())
