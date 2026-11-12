# Estado — nivel-ia (12/11/2026, ~15:45) — NADA PUBLICADO

## Feito (commits locais, sem remoto: 1a5a474 → 84e1cdb)
- Kit: ESCADA.md (AL1–AL5, como anotar n/p/g + erro grave + crítica, subir por degrau, descer, sem contradição), fichas PT/EN/ES (kit/ficha-papel*.html, cabeçalhos sem vírgula, mapeados por medir/nivel.py chave_coluna), papel-modelo.csv, medir/nivel.py (Claude Code + ~/.codex*, todas as conexões + as da ficha, decidir() por degrau atual, crítica por ficha ou palavra, relatório só com ficha), systemd (instalar.sh NUNCA rodado), 42 testes (`python3 tests/run.py`).
- Guia PT/EN/ES montado (scratchpad: corpo-pt.html + monta.py + fixvis.py + traduz-guia.sh em /tmp/claude-1000/-home-nmaldaner-projetos-wifi/1d269469-b102-4968-8f8d-be1ad8a9a55e/scratchpad/ — temporário; se sumiu, editar guia/index.html direto e retraduzir em 2 partes pelo inema-traduz). 6 banners + capa conferidos.
- Revisores 1–5: 6, 7, 5, 6, 6 (todos registrados em revisor-nota.py). Ciclo de revisão ENCERRADO (advisor): próximo revisor só bloqueia hero, escala 1–5, texto de evolução ou comando que falha.

## BLOQUEIOS antes de publicar
1. **75,4% não validado (fora da faixa 55–72% do goal).** 1.202 sessões (354,8 h) marcadas automáticas com humanos ≥ 2 e sem via_bot; 171,7 h em ~/projetos/wifi com 1º pedido de conversa do Nei (link artifact + YouTube). As sessões Claude do wifi são entrypoint "cli" → suspeita: são do Codex (fonte codex, originator codex_exec chamado pelo Claude) ou outro caminho. Próximo passo: `python3 -c` em registro/sessoes.json filtrando automatica & humanos>=2 & not via_bot, agrupar por `fonte` e `arquivo`; corrigir a regra (positiva: Claude `sdk-*` = automático; Codex `codex_exec` = automático só se não houver conversa real), rerodar varrer/relatorio.
2. **Exemplo e "Caso real" velhos:** TAREFAS_PADRAO mudou (nova crítica "Clientes e dinheiro"; `client`/`pago` são substrings perigosas — "MCP client", "apagou": trocar por palavras com borda). Regerar exemplo/relatorio-agregado.json e atualizar números do Caso real nos 3 idiomas; TIRAR a frase "E-mail e agenda 49%".
3. Rodar `sh systemd/instalar.sh` uma vez.

## Depois
- gh repo create inematds/nivel-ia --public; push via SSH (tem .github/workflows); Pages build_type=workflow; 3 guias + 3 fichas → 200.
- atualiza-portal (com EN/ES); postar-telegram INEMA.AGENTES.
- Vídeo: perguntar ao Nei se o vídeo com avatar "Qual o nível que você domina a IA?" (explicavideos/textos/nivel-ia, cadeia em "entrega") é o vídeo do kit; não fazer outro sem ele dizer.
- Perguntar ao Nei: o card/timer/repo antigo niveis-autonomia (não mexido).
