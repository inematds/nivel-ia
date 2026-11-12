# nivel-ia: What level is AI at in your work?

[![AI ladder: AL1 to AL5](guia/assets/banner-en.jpg)](https://inematds.github.io/nivel-ia/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

Without measuring, you don’t know what you still do by hand, what AI already does on its own, or which doors you’ve opened for it. This kit gives you a five-level scale, from AL1 (you do it yourself) to AL5 (AI runs on its own), and two ways to measure: a paper form that works for anyone and any AI, and a program that reads Claude Code and Codex logs on your computer and records every connection used. In the end, you’ll know what level each task is at, which one can move up now, and when to move down. To get started, all you need to do is print the form.

## 📖 User guide

Full guide (landing page + step-by-step instructions): **https://inematds.github.io/nivel-ia/guia/en/**

## In detail

An open, free kit to measure how much of your work AI already does, task by task, on the **AL1 to AL5 ladder**. Measure **on paper** (a form to print) or **automatically** (a program reads Claude Code and Codex logs on your machine). Both record **all connections** used by AI and show **which tasks can move up a level** and when to move down.

| Level | What it means |
|---|---|
| AL1 | You do it yourself. AI isn’t involved. |
| AL2 | AI helps: you ask, it answers, you do the work. |
| AL3 | AI collaborates: you work together, step by step, and you lead. |
| AL4 | AI leads, and you just review before it goes out. |
| AL5 | AI runs on its own, with a schedule, rules, and an alert. |

The complete ladder, including **how to move up each level and when to move down**, is in [ESCADA.md (in Portuguese)](ESCADA.md).

## The process, start to finish

Who does what: 🧠 you · ⚙️ script or timer

1. 🧠 **Read the ladder** and choose 3 tasks you do every week: [ESCADA.md (in Portuguese)](ESCADA.md).
2. 🧠 **On paper:** print the form (https://inematds.github.io/nivel-ia/kit/ficha-papel.en.html) and record one line per task (date, task, critical? y/n, level 1 to 5, minutes, connection used, fixed? n/p/g, serious error? y/n). It works with any AI and for work you do without AI (AL1).
3. 🧠 **Enter the form data** (optional): copy `kit/papel-modelo.csv` to `registro/papel.csv` and fill it in. Check with `python3 medir/nivel.py papel`.
4. ⚙️ **Automatic:** `python3 medir/nivel.py varrer --dias 30` reads Claude Code and Codex logs on this machine and saves them to `registro/sessoes.json`.
5. ⚙️ **Report:** `python3 medir/nivel.py relatorio` builds the ladder, tasks, next level for each task, connections, and “who can move up now” in `registro/relatorio.md` (including the paper form if one exists). The program’s report is in Portuguese.
6. ⚙️ **All connections:** `python3 medir/nivel.py conexoes` lists each program, site, service, agent, and skill, with the first and last time used.
7. ⚙️ **Run automatically every day:** `sh systemd/instalar.sh` enables a timer at 06:20 that repeats steps 4 and 5 and stores the history in `registro/historico.jsonl`.
8. 🧠 **Once a week:** read the report, choose ONE task to move up a level (criteria in ESCADA.md) and move down any task with a serious error.

## Requirements

Terminal, Python 3.9 or newer (standard library only, nothing to install), and git to download (or download the ZIP: https://github.com/inematds/nivel-ia/archive/refs/heads/main.zip). Linux or macOS (on Windows, use WSL). The timer uses systemd (Linux). No network, no API: nothing leaves your machine.

## What automatic measurement can and can’t see

- **Can see:** Claude Code sessions (`~/.claude/projects`) and Codex sessions (`~/.codex*/sessions`), how many messages you sent, how many AI actions, how much time, which programs, sites, services (MCP), agents, and skills it used, and which actions had an effect outside the machine (publishing, sending, uploading).
- **Can’t see:** what you do without AI (AL1: form only), other AIs (ChatGPT in a browser: form), whether you approved in the prompt, or whether AI got it right (“fixed?” column on the form).
- **How it assigns a level:** a session started by script, bot, or schedule (`claude -p`, `codex exec`) = AL5; a request you send through a bot (Telegram) = AL4; your terminal conversation: 15 or more AI actions per message from you = AL4, 5 to 14 = AL3, fewer = AL2 (a one-off question is AL2).
- **Moving up and down:** determined by the form’s “fixed?” (n/p/g) and “serious error?” (s/n) columns. AL1→AL2: no criteria; AL2→AL3: at most 1 major correction in the last 10 times; AL3→AL4: at most 2 in 20; AL4→AL5: at most 2 in 50 and no serious errors. Move down: 1 serious error or 3 major corrections in the last 10. Only entries at the current level count (when the level changes, the count starts over). A critical task (marked on the form or recognized by words such as publish, client, server, email…) stops at AL4. Without a form, the report lists the task as a candidate and says how many times to record it. Details in [ESCADA.md (in Portuguese)](ESCADA.md). The limits are at the top of `medir/nivel.py`.
- **Tasks:** grouped by keywords from the first request. To use your own, copy `medir/tarefas.exemplo.json` to `medir/tarefas.json` and edit it (format: `[["Task name", critical true/false, ["word", "another"]]]`). Critical tasks stop at AL4.

## Real-world example

[exemplo/relatorio-agregado.json (in Portuguese)](exemplo/relatorio-agregado.json): measurement of Nei Maldaner’s (INEMA) work over 30 days, with totals only (no prompts, folders, or sites).

## Tests

`python3 tests/run.py` (36 tests with fake logs; nothing from your machine).

## Privacy

`registro/` is excluded from git. The first request in each session is stored briefly, with keys, emails, and long numbers replaced by `[hidden]`.

MIT License · open and free kit · [inema.club](https://inema.club)