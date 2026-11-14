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
8. ⚙️ **Certificado:** `python3 medir/certificado.py --nome "Seu Nome"` gera `registro/certificado-AAAA-MM-DD.html`: degrau, escada AL1–AL5, tarefas, evolução semana a semana e projeção (1, 3 e 6 meses). Abre no navegador e vira PDF no botão. Período maior: `nivel.py --registro /tmp/n90 varrer --dias 90`, `nivel.py --registro /tmp/n90 relatorio` e `certificado.py --nome "Seu Nome" --registro /tmp/n90`.
8b. ⚙️ **Trabalho automático (opcional, Linux):** `python3 medir/motores.py` mede o que roda sem conversa nenhuma (timers do systemd, placar `rodadas.jsonl`, publicações do yt-pubx): motores, vigias, acerto e vídeos publicados, com as horas à mão estimadas em `registro/motores-minutos.json`. Depois `certificado.py --nome "Seu Nome" --motores` acrescenta a 2ª folha "Além da IA: o que roda sozinho". Outras máquinas (VPS): `motores.py --juntar root@host --chave ~/.ssh/chave` (mede lá por SSH, só leitura, sem deixar arquivo), depois `motores.py --geral` e `certificado.py --nome "Seu Nome" --geral --motores`. Conta também o cron e os serviços sempre ligados (Docker, pm2, units próprias); timers que vêm com o sistema (apt, logrotate…) ficam de fora.
9. ⚙️ **Várias máquinas (opcional):** em cada máquina, o passo 8 grava, ao lado do certificado da máquina, o arquivo `medicao-<máquina>-AAAA-MM-DD.json` (só números, conexões e tarefa; sem o texto dos pedidos e sem as pastas). Numa máquina só, junte: `python3 medir/nivel.py juntar medicao-notebook-*.json medicao-pc-*.json` (ou direto pelo caminho: `juntar usuario@host:/caminho/do/registro`, com `--chave` se precisar), depois `nivel.py relatorio --geral` e `certificado.py --nome "Seu Nome" --geral` → `registro/certificado-geral-AAAA-MM-DD.html` ("de N máquinas"). A mesma conversa nunca conta duas vezes. `nivel.py maquinas` lista as juntadas; `--tirar NOME` tira uma. Nome da máquina: `varrer --maquina "Notebook"` (padrão: o hostname).
10. 🧠 **Uma vez por semana:** leia o relatório, escolha UMA tarefa para subir um degrau (critérios em ESCADA.md) e desça a que errou feio.

## 🎓 Certificado: passo a passo

Uma página com o % do seu trabalho conduzido pela IA, a escada AL1–AL5, as tarefas principais, a evolução semana a semana e a projeção para 1, 3 e 6 meses. É HTML: abre em qualquer navegador e vira PDF no botão "Salvar em PDF".

**Jeito mais fácil (forma B): peça à sua IA.** Abra o Claude Code ou o Codex e cole (troque o nome). Dados confidenciais? Use o jeito do terminal, logo abaixo (veja Privacidade).

> Baixe o kit https://github.com/inematds/nivel-ia numa pasta nivel-ia (se já existir, use ela), meça os meus últimos 30 dias com `python3 medir/nivel.py varrer --dias 30` e `python3 medir/nivel.py relatorio`, gere o meu certificado com `python3 medir/certificado.py --nome "Seu Nome"` e abra o certificado no navegador. No fim, me diga onde ficaram o certificado e o relatório e resuma em 3 linhas o que deu. Não abra o arquivo registro/sessoes.json e não envie os meus dados para nenhum outro serviço nem site.

**Você mesmo, comando por comando** (Linux ou Mac; no Windows, WSL; Python 3.9+; ter usado o Claude Code ou o Codex nesta máquina):

```bash
git clone https://github.com/inematds/nivel-ia && cd nivel-ia
python3 medir/nivel.py varrer --dias 30          # 1. mede os últimos 30 dias (nada sai da máquina)
python3 medir/nivel.py relatorio                 # 2. monta o relatório
python3 medir/certificado.py --nome "Seu Nome"   # 3. gera o certificado (em inglês/espanhol: --lang en / --lang es)
xdg-open registro/certificado-*.html             # 4. abre (no Mac: open) → botão "Salvar em PDF"
```

Período maior (ex.: 90 dias), sem mexer no registro diário: `python3 medir/nivel.py --registro /tmp/n90 varrer --dias 90`, `python3 medir/nivel.py --registro /tmp/n90 relatorio` e `python3 medir/certificado.py --nome "Seu Nome" --registro /tmp/n90`. O Claude Code apaga registros com mais de 30 dias, a não ser que você aumente o `cleanupPeriodDays`; o que já foi apagado não volta. Se os registros cobrirem menos dias do que o pedido, o medidor avisa no terminal, no relatório e no certificado.

**Onde ficam os arquivos**

| Arquivo | O que é |
|---|---|
| `registro/certificado-AAAA-MM-DD.html` | O certificado (abra no navegador → "Salvar em PDF") |
| `registro/relatorio.md` | O relatório completo: escada, tarefas, próximo degrau, quem pode subir, conexões |
| `registro/relatorio.json` | Os mesmos números em dados (o certificado lê daqui) |
| `registro/sessoes.json` | A medição sessão por sessão (só na sua máquina, fora do git) |

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

`python3 tests/run.py` (46 testes com logs falsos, nada da sua máquina).

## Privacidade

**Duas formas de rodar.** O medidor é Python puro e roda só na sua máquina, sem internet. **A. Pelo terminal**: você roda os comandos e abre o certificado; nada sai do computador. **B. Pedindo à sua IA**: o Claude Code ou o Codex roda os comandos e lê o relatório para resumir, e essa leitura passa pelo servidor do provedor (Anthropic ou OpenAI), como qualquer sessão. O relatório traz os nomes das tarefas e as conexões (programas, agentes, skills e sites). Esses nomes podem revelar o nome de um cliente ou de um projeto. **Dados confidenciais (trabalho de cliente, sigilo): use a forma A.**

`registro/` fica fora do git. O primeiro pedido de cada sessão é guardado curto e com chaves, e-mails e números longos trocados por `[oculto]`.

Licença MIT · kit aberto e gratuito · [inema.club](https://inema.club)
