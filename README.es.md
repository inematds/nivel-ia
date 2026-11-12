# nivel-ia: ¿en qué escalón está la IA en tu trabajo?

[![Escalera de la IA: AL1 a AL5](guia/assets/banner-es.jpg)](https://inematds.github.io/nivel-ia/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

Sin medir, no sabes qué sigues haciendo a mano, qué ya hace la IA por su cuenta y qué puertas le abriste. Este kit te da una escala de cinco escalones, desde AL1 (lo haces por tu cuenta) hasta AL5 (la IA funciona sola), y dos formas de medir: una ficha de papel, que sirve para cualquier persona y cualquier IA, y un programa que lee los registros de Claude Code y Codex en tu computadora y anota cada conexión utilizada. Al final, sabes en qué escalón está cada tarea, cuál puede subir ahora y cuándo bajar. Para empezar, basta con imprimir la ficha.

El informe del programa se genera en portugués. La ficha acepta los nombres de columna y las respuestas y/yes/sí del idioma.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/nivel-ia/guia/es/**

## En detalle

Kit abierto y gratuito para medir cuánto de tu trabajo ya hace la IA, tarea por tarea, en la **escalera AL1 a AL5**. Puedes medir **en papel** (una ficha para imprimir) o **automáticamente** (un programa lee los registros de Claude Code y Codex en tu máquina). Ambos anotan **todas las conexiones** que usó la IA e indican **quién puede subir un escalón** y cuándo bajar.

| Escalón | Qué es |
|---|---|
| AL1 | Lo haces por tu cuenta. La IA no interviene. |
| AL2 | La IA ayuda: preguntas, responde y tú lo haces. |
| AL3 | La IA colabora: trabajan juntos, paso a paso, tú diriges. |
| AL4 | La IA dirige y tú solo revisas antes de que salga. |
| AL5 | La IA funciona sola, con horario, reglas y alarma. |

La escalera completa, con **cómo subir cada escalón y cuándo bajar**, está en [ESCADA.md](ESCADA.md) (en portugués).

## El proceso, de principio a fin

Quién lo hace: 🧠 tú · ⚙️ script o temporizador

1. 🧠 **Lee la escalera** y elige 3 tareas que haces todas las semanas: [ESCADA.md](ESCADA.md) (en portugués).
2. 🧠 **En papel:** imprime la ficha (https://inematds.github.io/nivel-ia/kit/ficha-papel.es.html) y anota una línea por tarea (fecha, tarea, escalón del 1 al 5, minutos, conexión utilizada, ¿corregí? n/p/g, ¿error grave? s/n). Sirve para cualquier IA y para lo que haces sin IA (AL1).
3. 🧠 **Escribe los datos de la ficha** (opcional): copia `kit/papel-modelo.csv` en `registro/papel.csv` y complétalo. Comprueba con `python3 medir/nivel.py papel`.
4. ⚙️ **Automático:** `python3 medir/nivel.py varrer --dias 30` lee los registros de Claude Code y Codex de esta máquina y los guarda en `registro/sessoes.json`.
5. ⚙️ **Informe:** `python3 medir/nivel.py relatorio` organiza la escalera, las tareas, el próximo escalón de cada una, las conexiones y "quién puede subir ahora" en `registro/relatorio.md` (también incluye la ficha de papel, si existe).
6. ⚙️ **Todas las conexiones:** `python3 medir/nivel.py conexoes` enumera cada programa, sitio, servicio, agente y skill, con la primera y la última vez que se usó.
7. ⚙️ **Todos los días, automáticamente:** `sh systemd/instalar.sh` activa un temporizador a las 06:20 que repite los pasos 4 y 5 y guarda el historial en `registro/historico.jsonl`.
8. 🧠 **Una vez por semana:** lee el informe, elige UNA tarea para subir un escalón (criterios en ESCADA.md) y baja la que tuvo errores graves.

## Requisitos

Terminal, Python 3.9 o posterior (solo biblioteca estándar, sin instalar nada) y git para descargar (o descarga el ZIP: https://github.com/inematds/nivel-ia/archive/refs/heads/main.zip). Linux o macOS (en Windows, usa WSL). El temporizador usa systemd (Linux). Sin conexión, sin API: nada sale de tu máquina.

## Qué muestra y qué no muestra la medición automática

- **Muestra:** sesiones de Claude Code (`~/.claude/projects`) y Codex (`~/.codex*/sessions`), cuántos mensajes tuyos, cuántas acciones de la IA, cuánto tiempo, qué programas, sitios, servicios (MCP), agentes y skills usó, y qué acciones tuvieron efecto fuera de la máquina (publicar, enviar, subir).
- **No muestra:** lo que haces sin IA (AL1: solo en la ficha), otras IA (ChatGPT en el navegador: ficha), si aprobaste en el prompt ni si la IA acertó (columna "¿corregí?" de la ficha).
- **Cómo decide el escalón:** sesión iniciada por script, bot u horario (`claude -p`, `codex exec`) = AL5; pedido tuyo hecho por medio del bot (Telegram) = AL4; conversación tuya en la terminal: 15 o más acciones de la IA por mensaje tuyo = AL4, de 5 a 14 = AL3, menos = AL2 (una pregunta aislada es AL2).
- **Subir y bajar:** se verifican con las columnas "¿corregí?" (n/p/g) y "¿error grave?" (s/n) de la ficha. AL1→AL2 sin criterio; AL2→AL3: como máximo 1 corrección grande en las últimas 10 veces; AL3→AL4: como máximo 2 en 20; AL4→AL5: como máximo 2 en 50 y ningún error grave. Bajar: 1 error grave o 3 correcciones grandes en las últimas 10 veces. Sin ficha, el informe indica la tarea como candidata y dice cuántas veces hay que anotarla. Más detalles en [ESCADA.md](ESCADA.md) (en portugués). Los límites están al inicio de `medir/nivel.py`.
- **Tareas:** agrupadas por palabras clave del primer pedido. Para usar las tuyas, copia `medir/tarefas.exemplo.json` en `medir/tarefas.json` y edítalo (formato `[["Nombre de la tarea", crítica true/false, ["palabra", "otra"]]]`). Una tarea crítica se detiene en AL4.

## Ejemplo real

[exemplo/relatorio-agregado.json](exemplo/relatorio-agregado.json) (en portugués): medición del trabajo de Nei Maldaner (INEMA) durante 30 días, solo con totales (sin pedidos, carpetas ni sitios).

## Pruebas

`python3 tests/run.py` (31 pruebas con registros falsos, nada de tu máquina).

## Privacidad

`registro/` queda fuera de git. El primer pedido de cada sesión se guarda de forma breve y se reemplazan las claves, los correos electrónicos y los números largos por `[oculto]`.

Licencia MIT · kit abierto y gratuito · [inema.club](https://inema.club)