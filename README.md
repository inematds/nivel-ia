# nivel-ia: em que degrau a IA está no seu trabalho?

[English](README.en.md) · [Español](README.es.md) · **Guia:** https://inematds.github.io/nivel-ia/guia/

Kit aberto e gratuito para medir quanto do seu trabalho a IA já faz, tarefa por tarefa, na **escada AL1 a AL5**. Você mede **no papel** (uma ficha para imprimir) ou **automaticamente** (um programa lê os registros do Claude Code e do Codex na sua máquina). Os dois anotam **todas as conexões** que a IA usou e dizem **quem pode subir um degrau** e quando descer.

| Degrau | O que é |
|---|---|
| AL1 | Você faz sozinho. A IA não entra. |
| AL2 | A IA ajuda: você pergunta, ela responde, você faz. |
| AL3 | A IA colabora: juntos, passo a passo, você conduz. |
| AL4 | A IA conduz e você só revisa antes de sair. |
| AL5 | A IA roda sozinha, com horário, regra e alarme. |

A escada completa, com **como subir cada degrau e quando descer**, está em [ESCADA.md](ESCADA.md).

## O processo, do início ao fim

Quem faz: 🧠 você · ⚙️ script ou timer

1. 🧠 **Leia a escada** e escolha 3 tarefas que você faz toda semana: [ESCADA.md](ESCADA.md).
2. 🧠 **No papel:** imprima [kit/ficha-papel.html](kit/ficha-papel.html) e anote uma linha por tarefa (data, tarefa, degrau 1 a 5, minutos, conexão usada, corrigi?). Serve para qualquer IA e para o que você faz sem IA (AL1).
3. 🧠 **Digite a ficha** (opcional): copie `kit/papel-modelo.csv` para `registro/papel.csv` e vá preenchendo. Confira com `python3 medir/nivel.py papel`.
4. ⚙️ **Automático:** `python3 medir/nivel.py varrer --dias 30` lê os logs do Claude Code e do Codex desta máquina e grava `registro/sessoes.json`.
5. ⚙️ **Relatório:** `python3 medir/nivel.py relatorio` monta a escada, as tarefas, o próximo degrau de cada uma, as conexões e "quem pode subir agora" em `registro/relatorio.md` (junta a ficha de papel se existir).
6. ⚙️ **Todas as conexões:** `python3 medir/nivel.py conexoes` lista cada programa, site, serviço, agente e skill, com a primeira e a última vez.
7. ⚙️ **Todo dia sozinho:** `sh systemd/instalar.sh` liga um timer às 06:20 que repete os passos 4 e 5 e guarda o histórico em `registro/historico.jsonl`.
8. 🧠 **Uma vez por semana:** leia o relatório, escolha UMA tarefa para subir um degrau (critérios em ESCADA.md) e desça a que errou feio.

## Requisitos

Python 3.9 ou mais novo, só biblioteca padrão, sem instalar nada. Linux ou macOS (no Windows, use o WSL). O timer usa systemd (Linux). Sem rede, sem API: nada sai da sua máquina.

## O que a medição automática vê e não vê

- **Vê:** sessões do Claude Code (`~/.claude/projects`) e do Codex (`~/.codex*/sessions`), quantas mensagens suas, quantas ações da IA, quanto tempo, que programas, sites, serviços (MCP), agentes e skills ela usou, e quais ações tiveram efeito fora da máquina (publicar, enviar, subir).
- **Não vê:** o que você faz sem IA (AL1: só na ficha), outras IAs (ChatGPT no navegador: ficha), se você aprovou no prompt, e se a IA acertou (coluna "corrigi?" da ficha).
- **Como decide o degrau:** sessão sem conversa (timer, script, bot) = AL5; com conversa, 15 ou mais ações da IA por mensagem sua = AL4, 5 a 14 = AL3, menos = AL2. Os limites ficam no topo de `medir/nivel.py`.
- **Tarefas:** agrupadas por palavras-chave do primeiro pedido. Para usar as suas, crie `medir/tarefas.json` no formato `[["Nome da tarefa", crítica true/false, ["palavra", "outra"]]]`. Tarefa crítica para no AL4.

## Exemplo real

[exemplo/relatorio-agregado.json](exemplo/relatorio-agregado.json): a medição do trabalho do Nei Maldaner (INEMA) em 30 dias, só com totais (sem pedidos, pastas nem sites).

## Testes

`python3 tests/run.py` (logs falsos, nada da sua máquina).

## Privacidade

`registro/` fica fora do git. O primeiro pedido de cada sessão é guardado curto e com chaves, e-mails e números longos trocados por `[oculto]`.

Licença MIT · kit aberto e gratuito · [inema.club](https://inema.club)

## Self-learning

Quando o Nei corrigir ou um erro for achado, escreva a lição como uma linha no topo de **Lessons**, antes de seguir.

## Lessons

- A escada é AL1 a AL5 (vídeo do Nei de 12/11/2026). Nunca 0 a 4. (12/11/2026)
