---
tipo: corpus
estado: activo
prioridad_categoria: reputacion
activo_legado: conocimiento
actualizado: 2026-06-15
---

# Corpus inicial - apoyos IA para investigar

## Criterio de lectura

Cada ficha distingue:

1. hecho observado;
2. patron util;
3. etapa de investigacion;
4. riesgo;
5. resguardo;
6. decision para Investigadopedia.

## Fichas iniciales

| Fuente | Tipo | Etapas | Hecho observado | Patron util | Riesgo | Resguardo | Decision |
|---|---|---|---|---|---|---|---|
| Feynman | agente open source | literatura, escritura, auditoria | Declara agentes separados: researcher, reviewer, writer, verifier | Separar roles de busqueda, revision, redaccion y verificacion | Delegar investigacion completa al agente | Exigir sidecar de procedencia y decision humana | Benchmark externo |
| Elicit | SaaS investigacion | literatura | Declara apoyo a protocolo, busqueda, screening, extraccion y sintesis | Convertir revision en flujo por pasos | Sesgo de seleccion, extraccion incompleta | Validar busquedas, criterios y papers excluidos | Ficha de revision sistematica |
| Consensus | buscador academico IA | literatura | Busca y sintetiza literatura revisada por pares | Respuesta con trazabilidad a papers | Lectura rapida sin evaluar cobertura | Revisar papers base y no solo sintesis | Fuente para exploracion inicial |
| SciSpace | asistente investigacion | literatura, escritura | Ofrece revision de literatura y chat con PDFs | Lectura guiada de corpus | Confiar en resumen sin leer metodo/resultados | Citar solo despues de verificar PDF | Ficha de lectura asistida |
| ResearchRabbit | mapa literatura | literatura | Mapea papers, autores y conexiones | Descubrimiento por red de citacion | Popularidad como proxy de relevancia | Combinar con busqueda sistematica | Modulo de mapeo |
| Litmaps | mapa literatura | literatura | Visualizacion, monitoreo y colaboracion | Mantener vigilancia bibliografica | Sobrevalorar novedades | Registrar criterio de inclusion | Modulo de vigilancia |
| NotebookLM | cuaderno con fuentes | literatura, escritura | Trabaja sobre fuentes cargadas por usuario | Sintesis sobre corpus cerrado | Si el corpus es malo, la respuesta tambien | Curar fuentes antes de consultar | Posible integracion futura |
| Open Deep Research | repo open source | literatura | Agente simple de investigacion iterativa con busqueda web | Transparencia educativa por codigo pequeno | Calidad depende de buscadores/modelos | Usar como referencia didactica, no como autoridad | Referencia tecnica |

## Glosario hispanoamericano inicial

| Termino ingles | Traduccion recomendada | Nota editorial |
|---|---|---|
| deep research | investigacion profunda asistida | No implica autonomia total ni validez automatica |
| literature mapping | mapeo de literatura | Diferenciar de revision sistematica |
| verifier | verificador de fuentes y trazabilidad | Decir que verifica: URL, cita, claim o dato |
| simulated peer review | revision simulada por pares | Siempre declarar que no reemplaza pares reales |
| human-in-the-loop | validacion humana situada | No basta "humano en el loop"; debe decidir con criterio |
| cognitive offloading | delegacion cognitiva | Riesgo central cuando IA reemplaza juicio |
| provenance | trazabilidad de fuentes y decisiones | Debe registrar origen, estado y verificacion |

