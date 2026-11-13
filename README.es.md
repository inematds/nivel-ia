# nivel-ia: ¿en qué peldaño está la IA en tu trabajo?

[![Escalera de la IA: AL1 a AL5](guia/assets/banner-es.jpg)](https://inematds.github.io/nivel-ia/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

Sin medir, no sabes qué sigues haciendo a mano, qué ya hace la IA por sí sola ni qué puertas le has abierto. Este kit ofrece una escala de cinco peldaños, desde AL1 (tú lo haces por tu cuenta) hasta AL5 (la IA funciona sola), y dos formas de medir: una ficha en papel, que sirve para cualquier persona y cualquier IA, y un programa que lee los registros de Claude Code y Codex en tu computadora y anota cada conexión usada. Al final, sabes en qué peldaño está cada tarea, cuál puede subir ahora y cuándo debe bajar. Para empezar, basta con imprimir la ficha.

## 📖 Guía de uso

Guía completa (página de presentación + paso a paso): **https://inematds.github.io/nivel-ia/guia/es/**

## En detalle

Kit abierto y gratuito para medir cuánto de tu trabajo ya hace la IA, tarea por tarea, en la **escalera AL1 a AL5**. Puedes medir **en papel** (una ficha para imprimir) o **automáticamente** (un programa lee los registros de Claude Code y Codex en tu computadora). Ambos registran **todas las conexiones** que usó la IA e indican **quién puede subir un peldaño** y cuándo debe bajar.

| Peldaño | Qué significa |
|---|---|
| AL1 | Tú lo haces por tu cuenta. La IA no participa. |
| AL2 | La IA ayuda: tú preguntas, ella responde y tú haces el trabajo. |
| AL3 | La IA colabora: trabajan juntos paso a paso y tú diriges. |
| AL4 | La IA dirige y tú solo revisas antes de que salga. |
| AL5 | La IA funciona sola, con horario, regla y alarma. |

La escalera completa, con **cómo subir cada peldaño y cuándo bajar**, está en [ESCADA.md (en portugués)](ESCADA.md).

## El proceso, de principio a fin

Quién lo hace: 🧠 tú · ⚙️ script o temporizador

1. 🧠 **Lee la escalera** y elige 3 tareas que haces todas las semanas: [ESCADA.md (en portugués)](ESCADA.md).
2. 🧠 **En papel:** imprime la ficha (https://inematds.github.io/nivel-ia/kit/ficha-papel.es.html) y anota una línea por tarea (fecha, tarea, ¿crítica? s/n, peldaño 1 a 5, minutos, conexión usada, ¿corregí? n/p/g, ¿error grave? s/n). Sirve para cualquier IA y para lo que haces sin IA (AL1).
3. 🧠 **Digitaliza la ficha** (opcional): copia `kit/papel-modelo.csv` en `registro/papel.csv`, ábrelo en una hoja de cálculo, escribe las líneas y guárdalo como CSV. Compruébalo con `python3 medir/nivel.py papel`. Si solo usas la ficha, puedes omitir los pasos 4 y 6: el informe del programa sale en portugués.
4. ⚙️ **Automático:** `python3 medir/nivel.py varrer --dias 30` lee los registros de Claude Code y Codex de esta computadora y los guarda en `registro/sessoes.json`.
5. ⚙️ **Informe:** `python3 medir/nivel.py relatorio` genera la escalera, las tareas, el próximo peldaño de cada una, las conexiones y «quién puede subir ahora» en `registro/relatorio.md` (combina la ficha en papel si existe).
6. ⚙️ **Todas las conexiones:** `python3 medir/nivel.py conexoes` enumera cada programa, sitio, servicio, agente y skill, con la primera y la última vez que se usaron.
7. ⚙️ **Todos los días, automáticamente:** `sh systemd/instalar.sh` activa un temporizador a las 06:20 que repite los pasos 4 y 5 y guarda el historial en `registro/historico.jsonl`.
8. 🧠 **Una vez por semana:** lee el informe, elige UNA tarea para subir un peldaño (criterios en ESCADA.md) y baja la que tuvo un error grave.

## Requisitos

Terminal, Python 3.9 o posterior (solo biblioteca estándar, sin instalar nada) y git para descargarlo (o descarga el ZIP: https://github.com/inematds/nivel-ia/archive/refs/heads/main.zip). Linux o macOS (en Windows, usa WSL). El temporizador usa systemd (Linux). Sin red, sin API: nada sale de tu computadora.

## Qué ve y qué no ve la medición automática

- **Ve:** sesiones de Claude Code (`~/.claude/projects`) y de Codex (`~/.codex*/sessions`), cuántos mensajes enviaste, cuántas acciones hizo la IA, cuánto tiempo, qué programas, sitios y servicios (MCP), agentes y skills usó, y qué acciones tuvieron efecto fuera de la computadora (publicar, enviar, subir).
- **No ve:** lo que haces sin IA (AL1: solo en la ficha), otras IA (ChatGPT en el navegador: ficha), si aprobaste en el prompt ni si la IA acertó (columna «¿corregí?» de la ficha).
- **Cómo decide el peldaño:** una sesión iniciada por script, bot u horario (`claude -p`, `codex exec`) con hasta 2 mensajes = AL5 (3 o más = conversación); un pedido tuyo hecho por el bot (Telegram) = AL4; una conversación tuya en la terminal: 15 o más acciones de la IA por cada mensaje tuyo = AL4, de 5 a 14 = AL3, menos = AL2 (una pregunta suelta es AL2).
- **Subir y bajar:** se determina con las columnas «¿corregí?» (n/p/g) y «¿error grave?» (s/n) de la ficha. AL1→AL2 sin criterio; AL2→AL3: como máximo 1 corrección grande en las últimas 10 veces; AL3→AL4: como máximo 2 en 20; AL4→AL5: como máximo 2 en 50 y ningún error grave. Bajar: 1 error grave o 3 correcciones grandes en las últimas 10 veces. Solo cuentan las veces del peldaño actual (al cambiar de peldaño, el conteo empieza de nuevo). Una tarea crítica (marcada en la ficha o reconocida por palabras como publicar, cliente, servidor, correo electrónico…) se detiene en AL4. Sin ficha, el informe incluye la tarea como candidata e indica cuántas veces debes anotarla. Más detalles en [ESCADA.md (en portugués)](ESCADA.md). Los límites están al principio de `medir/nivel.py`.
- **Tareas:** se agrupan por palabras clave del primer pedido. Para usar las tuyas, copia `medir/tarefas.exemplo.json` en `medir/tarefas.json` y edítalo (formato `[["Nombre de la tarea", crítica true/false, ["palabra", "otra"]]]`). Las tareas críticas se detienen en AL4.

## Ejemplo real

[exemplo/relatorio-agregado.json (en portugués)](exemplo/relatorio-agregado.json): medición del trabajo de Nei Maldaner (INEMA) durante 30 días, solo con totales (sin pedidos, carpetas ni sitios).

## Pruebas

`python3 tests/run.py` (42 pruebas con registros falsos, nada de tu computadora).

## Privacidad

`registro/` queda fuera de git. Se guarda una versión breve del primer pedido de cada sesión, con las claves, los correos electrónicos y los números largos reemplazados por `[oculto]`.

Licencia MIT · kit abierto y gratuito · [inema.club](https://inema.club)