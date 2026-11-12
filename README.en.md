# nivel-ia: what level is AI at in your work?

[![The AI ladder: AL1 to AL5](guia/assets/banner-en.jpg)](https://inematds.github.io/nivel-ia/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

Without measuring, you don’t know what you still do by hand, what AI already does on its own, or which doors you’ve opened for it. This kit gives you a five-level scale, from AL1 (you do it yourself) to AL5 (AI runs on its own), and two ways to measure: a paper form that works for anyone and any AI, and a program that reads Claude Code and Codex logs on your computer and records every connection used. In the end, you’ll know what level each task is at, which one can move up now, and when to move down. To get started, just print the form.

## 📖 User guide

Full guide (landing page + step-by-step): **https://inematds.github.io/nivel-ia/guia/en/**

## In detail

Free and open kit for measuring how much of your work AI already does, task by task, on the **AL1 to AL5 ladder**. You can measure **on paper** (a form to print) or **automatically** (a program reads Claude Code and Codex logs on your machine). Both record **every connection** AI used and tell you **which tasks can move up a level** and when to move down.

| Level | What it is |
|---|---|
| AL1 | You do it yourself. AI isn’t involved. |
| AL2 | AI helps: you ask, it answers, you do the work. |
| AL3 | AI collaborates: you work together, step by step, and you lead. |
| AL4 | AI leads, and you only review before it goes out. |
| AL5 | AI runs on its own, with a schedule, rules, and alerts. |

The full ladder, including **how to move up each level and when to move down**, is in [ESCADA.md](ESCADA.md) (in Portuguese).

## The process, start to finish

Who does what: 🧠 you · ⚙️ script or timer

1. 🧠 **Read the ladder** and choose 3 tasks you do every week: [ESCADA.md](ESCADA.md) (in Portuguese).
2. 🧠 **On paper:** print the form (https://inematds.github.io/nivel-ia/kit/ficha-papel.en.html) and record one row per task (date, task, level 1 to 5, minutes, connection used, did I correct it? n/p/g, serious error? s/n). It works with any AI and for work you do without AI (AL1).
3. 🧠 **Enter the form data** (optional): copy `kit/papel-modelo.csv` to `registro/papel.csv` and fill it in. Check it with `python3 medir/nivel.py papel`.
4. ⚙️ **Automatic measurement:** `python3 medir/nivel.py varrer --dias 30` reads Claude Code and Codex logs on this machine and saves them to `registro/sessoes.json`.
5. ⚙️ **Report:** `python3 medir/nivel.py relatorio` builds the ladder, tasks, each task’s next level, connections, and “who can move up now” in `registro/relatorio.md` (it includes the paper form data if available). The program report is in Portuguese, and the form accepts that language’s column names and y/yes/sí values.
6. ⚙️ **All connections:** `python3 medir/nivel.py conexoes` lists every program, site, service, agent, and skill, with the first and last time used.
7. ⚙️ **Run automatically every day:** `sh systemd/instalar.sh` starts a timer at 06:20 that repeats steps 4 and 5 and saves the history to `registro/historico.jsonl`.
8. 🧠 **Once a week:** read the report, choose ONE task to move up a level (criteria in ESCADA.md), and move down any task that went badly.

## Requirements

Terminal, Python 3.9 or newer (standard library only; nothing to install), and git to download (or download the ZIP: https://github.com/inematds/nivel-ia/archive/refs/heads/main.zip). Linux or macOS (on Windows, use WSL). The timer uses systemd (Linux). No network, no API: nothing leaves your machine.

## What automatic measurement sees and doesn’t see

- **Sees:** Claude Code sessions (`~/.claude/projects`) and Codex sessions (`~/.codex*/sessions`), the number of your messages, the number of AI actions, how much time, which programs, sites, services (MCP), agents, and skills it used, and which actions had an effect outside the machine (publishing, sending, uploading).
- **Doesn’t see:** work you do without AI (AL1: form only), other AIs (ChatGPT in a browser: form), whether you approved in the prompt, or whether AI got it right (the form’s “did I correct it?” column).
- **How it assigns a level:** a session started by a script, bot, or schedule (`claude -p`, `codex exec`) = AL5; a request you make through a bot (Telegram) = AL4; a conversation you have in the terminal: 15 or more AI actions per message from you = AL4, 5 to 14 = AL3, fewer = AL2 (a single standalone question is AL2).
- **Moving up and down:** determined by the form’s “did I correct it?” (n/p/g) and “serious error?” (s/n) columns. AL1→AL2 has no criteria; AL2→AL3: at most 1 major correction in the last 10 times; AL3→AL4: at most 2 in 20; AL4→AL5: at most 2 in 50 and no serious errors. Move down after 1 serious error or 3 major corrections in the last 10. Without a form, the report lists the task as a candidate and says how many times to record it. Details in [ESCADA.md](ESCADA.md) (in Portuguese). The limits are at the top of `medir/nivel.py`.
- **Tasks:** grouped by keywords in the first request. To use your own, copy `medir/tarefas.exemplo.json` to `medir/tarefas.json` and edit it (format: `[["Task name", critical true/false, ["keyword", "another"]]]`). Critical tasks stop at AL4.

## Real example

[exemplo/relatorio-agregado.json](exemplo/relatorio-agregado.json) (in Portuguese): measurement of Nei Maldaner’s (INEMA) work over 30 days, with totals only (no requests, folders, or sites).

## Tests

`python3 tests/run.py` (31 tests with fake logs; nothing from your machine).

## Privacy

`registro/` is excluded from git. The first request in each session is stored in shortened form, with keys, emails, and long numbers replaced by `[oculto]`.

MIT License · free and open kit · [inema.club](https://inema.club)