# nivel-ia: em que degrau a IA está no seu trabalho?

[![Escada da IA: AL1 a AL5](guia/assets/banner.jpg)](https://inematds.github.io/nivel-ia/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Sem medir, você não sabe o que ainda faz na mão, o que a IA já faz sozinha e quais portas abriu para ela. Este kit dá uma régua de cinco degraus, do AL1 (você faz sozinho) ao AL5 (a IA roda sozinha), e duas formas de medir: uma ficha de papel, que serve para qualquer pessoa e qualquer IA, e um programa que lê os registros do Claude Code e do Codex no seu computador e anota cada conexão usada. No fim, você sabe em que degrau está cada tarefa, qual pode subir agora e quando descer. Para começar, basta imprimir a ficha.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/nivel-ia/guia/**

## Em detalhe

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
2. 🧠 **No papel:** imprima a ficha (https://inematds.github.io/nivel-ia/kit/ficha-papel.html) e anote uma linha por tarefa (data, tarefa, crítica? s/n, degrau 1 a 5, minutos, conexão usada, corrigi? n/p/g, erro grave? s/n). Serve para qualquer IA e para o que você faz sem IA (AL1).
3. 🧠 **Digite a ficha** (opcional): copie `kit/papel-modelo.csv` para `registro/papel.csv`, abra numa planilha, digite as linhas e salve como CSV. Confira com `python3 medir/nivel.py papel`. Quem só usa a ficha pode pular os passos 4 e 6: o relatório sai só com ela.
4. ⚙️ **Automático:** `python3 medir/nivel.py varrer --dias 30` lê os logs do Claude Code e do Codex desta máquina e grava `registro/sessoes.json`.
5. ⚙️ **Relatório:** `python3 medir/nivel.py relatorio` monta a escada, as tarefas, o próximo degrau de cada uma, as conexões e "quem pode subir agora" em `registro/relatorio.md` (junta a ficha de papel se existir).
6. ⚙️ **Todas as conexões:** `python3 medir/nivel.py conexoes` lista cada programa, site, serviço, agente e skill, com a primeira e a última vez.
7. ⚙️ **Todo dia sozinho:** `sh systemd/instalar.sh` liga um timer às 06:20 que repete os passos 4 e 5 e guarda o histórico em `registro/historico.jsonl`.
8. 🧠 **Uma vez por semana:** leia o relatório, escolha UMA tarefa para subir um degrau (critérios em ESCADA.md) e desça a que errou feio.

## Requisitos

Terminal, Python 3.9 ou mais novo (só biblioteca padrão, sem instalar nada) e git para baixar (ou baixe o ZIP: https://github.com/inematds/nivel-ia/archive/refs/heads/main.zip). Linux ou macOS (no Windows, use o WSL). O timer usa systemd (Linux). Sem rede, sem API: nada sai da sua máquina.

## O que a medição automática vê e não vê

- **Vê:** sessões do Claude Code (`~/.claude/projects`) e do Codex (`~/.codex*/sessions`), quantas mensagens suas, quantas ações da IA, quanto tempo, que programas, sites, serviços (MCP), agentes e skills ela usou, e quais ações tiveram efeito fora da máquina (publicar, enviar, subir).
- **Não vê:** o que você faz sem IA (AL1: só na ficha), outras IAs (ChatGPT no navegador: ficha), se você aprovou no prompt, e se a IA acertou (coluna "corrigi?" da ficha).
- **Como decide o degrau:** sessão aberta por script, bot ou horário (`claude -p`, `codex exec`) com até 2 mensagens = AL5 (3 ou mais = conversa); pedido seu feito pelo bot (Telegram) = AL4; conversa sua no terminal: 15 ou mais ações da IA por mensagem sua = AL4, 5 a 14 = AL3, menos = AL2 (uma pergunta solta é AL2).
- **Subir e descer:** conferidos pelas colunas "corrigi?" (n/p/g) e "erro grave?" (s/n) da ficha. AL1→AL2 sem critério; AL2→AL3: no máximo 1 correção grande nas últimas 10 vezes; AL3→AL4: no máximo 2 em 20; AL4→AL5: no máximo 2 em 50 e nenhum erro grave. Descer: 1 erro grave ou 3 correções grandes nas últimas 10. Só contam as vezes do degrau atual (mudou de degrau, a conta recomeça). Tarefa crítica (marcada na ficha ou reconhecida pelas palavras: publicar, cliente, servidor, e-mail…) para no AL4. Sem ficha, o relatório lista a tarefa como candidata e diz quantas vezes anotar. Detalhes em [ESCADA.md](ESCADA.md). Os limites ficam no topo de `medir/nivel.py`.
- **Tarefas:** agrupadas por palavras-chave do primeiro pedido. Para usar as suas, copie `medir/tarefas.exemplo.json` para `medir/tarefas.json` e edite (formato `[["Nome da tarefa", crítica true/false, ["palavra", "outra"]]]`). Tarefa crítica para no AL4.

## Exemplo real

[exemplo/relatorio-agregado.json](exemplo/relatorio-agregado.json): a medição do trabalho do Nei Maldaner (INEMA) em 30 dias, só com totais (sem pedidos, pastas nem sites).

## Testes

`python3 tests/run.py` (42 testes com logs falsos, nada da sua máquina).

## Privacidade

`registro/` fica fora do git. O primeiro pedido de cada sessão é guardado curto e com chaves, e-mails e números longos trocados por `[oculto]`.

Licença MIT · kit aberto e gratuito · [inema.club](https://inema.club)
