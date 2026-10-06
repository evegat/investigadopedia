---
tipo: entregable
estado: borrador_ejecutable
prioridad_categoria: reputacion
activo_legado: conocimiento
actualizado: 2026-06-15
referencia_externa:
  - "https://github.com/companion-inc/feynman"
  - "https://elicit.com/solutions/systematic-review"
  - "https://consensus.app/search/"
  - "https://scispace.com/"
---

# Investigadopedia Observatorio

## Formulacion breve

Investigadopedia Observatorio es una infraestructura abierta de curaduria, comparacion y auditoria metodologica de apoyos IA para investigar. Su proposito no es reemplazar al investigador ni producir papers automaticos, sino poner a disposicion una biblioteca viva de herramientas, prompts, flujos, casos, riesgos y resguardos para usar IA en investigacion con criterio, trazabilidad y responsabilidad.

La tesis del proyecto es simple: la IA puede acelerar etapas de investigacion, pero solo aporta valor academico si cada apoyo queda situado por etapa, con evidencia verificable, limites claros y decision humana registrada.

## Problema

El ecosistema actual esta fragmentado:

- hay buscadores academicos con IA, asistentes de PDF, agentes de deep research, mapas de literatura, copilotos de escritura y notebooks con fuentes;
- cada herramienta promete velocidad, pero no siempre explicita cobertura, sesgos, trazabilidad, privacidad o limites metodologicos;
- investigadores novatos tienden a mezclar formulacion, literatura, metodo, datos, analisis y escritura en un mismo chat;
- la friccion metodologica se pierde: la IA responde antes de que el diseno este suficientemente justificado.

Investigadopedia debe ordenar ese exceso como bien publico: no vender otra herramienta, sino curar el campo para que investigadores sepan que usar, cuando, con que resguardos y que no delegar.

## Diferenciacion

| Capa | Herramientas existentes | Investigadopedia Observatorio |
|---|---|---|
| Literatura | Buscan, resumen, extraen o mapean papers | Evalua para que etapa sirven, que validacion humana exigen y que sesgos abren |
| Agentes | Automatizan busqueda, escritura, revision o verificacion | Separa apoyo operativo de decision metodologica |
| Escritura | Mejoran redaccion o estructura | Impide redactar sin andamiaje aprobado |
| Curaduria | Listas de herramientas o reviews comerciales | Fichas con hecho observado, patron, traduccion hispana, riesgo y resguardo |
| Bien publico | SaaS cerrado o repos aislados | Corpus abierto, prompts auditables, prototipo clonable y rutas de contribucion |

## Taxonomia por etapa de investigacion

| Etapa | Apoyo IA razonable | Validacion humana obligatoria | Riesgo principal | Salida curada |
|---|---|---|---|---|
| Formulacion | Generar alternativas de pregunta, alcance y unidad de analisis | Pertinencia disciplinar, viabilidad y valor academico | Preguntas vagas o sobredimensionadas | Ficha problema-pregunta-alcance |
| Literatura | Buscar, mapear, resumir y extraer papers | Fuentes reales, criterios de inclusion, cobertura y sesgo de busqueda | Referencias falsas o seleccion sesgada | Matriz de literatura y vacios |
| Metodo | Comparar disenos y advertir inconsistencias | Atingencia entre pregunta, disciplina, datos y metodo | Metodo que no responde la pregunta | Justificacion metodologica |
| Datos | Sugerir estructura, variables, limpieza y resguardos | Acceso, calidad, permisos, privacidad y unidad de analisis | Sobreafirmacion desde datos debiles | Matriz objetivo-dato-analisis |
| Analisis | Proponer tecnicas, codigo y visualizaciones | Supuestos, interpretacion, causalidad y limites | Tecnica correcta para pregunta incorrecta | Plan de analisis validado |
| Escritura | Mejorar claridad, estructura y consistencia | Argumento, autoria, citas y evidencia | Homogeneizacion o falsa autoridad | Borrador con declaracion de uso IA |
| Auditoria | Detectar vacios, claims sin fuente y desalineaciones | Decision final del investigador o experto | Falsa seguridad por checklist automatico | Informe de coherencia y trazabilidad |

## Dataset inicial investigado

La version inicial del observatorio usa un corpus pequeno y verificable:

- Feynman: agente open source de investigacion con roles de researcher, reviewer, writer y verifier; benchmark para separar busqueda, revision, escritura y verificacion.
- Elicit: asistente para revision sistematica con soporte para protocolo, busqueda, screening, extraccion y sintesis.
- Consensus: buscador academico con IA sobre literatura revisada por pares.
- SciSpace: asistente para revisar literatura y conversar con PDFs.
- ResearchRabbit: herramienta de mapeo de literatura y relaciones de citacion.
- Litmaps: mapas dinamicos de literatura, monitoreo y colaboracion.
- NotebookLM: cuadernos con fuentes cargadas por el usuario; util para trabajar con corpus cerrado, pero dependiente de calidad de fuentes.

## Arquitectura del bien publico

1. **Corpus abierto**
   - fichas de herramientas;
   - fichas de papers;
   - casos de uso por etapa;
   - glosario hispanoamericano;
   - matriz de riesgos y resguardos.

2. **Prototipo de app**
   - catalogo curado;
   - filtros por etapa, licencia, privacidad y madurez;
   - chat auditor metodologico;
   - exportacion de ficha Markdown;
   - backend mock para servir datos y respuestas reproducibles.

3. **Paquete academico**
   - working paper;
   - articulo corto para blog academico;
   - paper de software si el prototipo se publica como repo abierto;
   - protocolo de evaluacion con usuarios.

4. **Gobernanza open source**
   - licencia MIT para codigo;
   - CC BY 4.0 para fichas y contenidos;
   - plantilla de contribucion;
   - revisiones por pares de fichas;
   - sidecar de trazabilidad para cada fuente relevante.

## Roadmap

### Fase 0: Corpus minimo y demo local

- Cerrar 12 fichas curadas.
- Implementar prototipo local con catalogo, chat mock y exportacion.
- Publicar README orientado a contribuidores.
- Preparar demo de 5 minutos.

### Fase 1: Validacion experta

- 5 entrevistas con investigadores, tesistas y docentes guia.
- 3 revisiones expertas: metodologia, bibliotecas/ciencia abierta, IA responsable.
- Medir si el observatorio ayuda a escoger herramientas sin delegar juicio.

### Fase 2: Publicacion abierta

- Repo GitHub con issues, roadmap y licencias.
- Post LSE Impact Blog o equivalente.
- Preprint metodologico.
- Si el software crece, preparar JOSS o Journal of Open Research Software.

### Fase 3: Financiamiento

- Vercel Open Source Program para hosting cuando reabra postulaciones.
- NVIDIA Inception si se constituye como startup/proyecto tecnico con necesidad de compute.
- Google Summer of Code via organizacion aliada o fundacion open source.
- Anthropic/OpenAI safety fellowships solo si el angulo se reformula como evaluacion, trazabilidad o oversight de agentes de investigacion.
- Fondos locales/universitarios: ciencia abierta, educacion superior, integridad academica y bienes publicos digitales.

## Criterio de termino de la siguiente iteracion

El proyecto avanza si quedan listos:

- corpus inicial con al menos 12 fuentes;
- prototipo local demostrable;
- paper borrador con problema, marco, metodo, contribucion y referencias;
- matriz de financiamiento y publicacion;
- paquete de evaluacion experta.

