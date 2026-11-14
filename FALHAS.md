# FALHAS — nivel-ia

Uma linha por falha, mais recente no topo.

| data | o que quebrou | menor correção | prompt \| infra |
|---|---|---|---|
| 2026-11-13 | Certificado da Tiza (7,7 h de uso) saiu sem gráfico: corte fixo de 10 h/semana zerava a curva | corte cai para 15 min/semana quando nenhuma semana passa de 10 h, com nota "pouco uso" | infra |
| 2026-11-13 | "Salvar em PDF" quebrava o certificado em 2 páginas: A4 deitado (1123 px) caía no `@media (max-width:1150px)` | media query só `screen` | infra |
