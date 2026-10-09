---
tipo: proyecto
codigo: EDI001
subtipo: paper
estado: movimiento
prioridad_categoria: reputacion
activo_legado: conocimiento
portafolio:
es_portafolio: false
personas:
  - "[[Valentina Cariaga]]"
proximo_paso: "Levantar y curar fuentes sobre investigacion asistida por IA, partiendo por Feynman, y traducir sus patrones a lenguaje hispanoamericano"
criterio_terminado: "Biblioteca curada con fichas de fuentes, conceptos acunados, traduccion/adaptacion hispana y patrones reutilizables para Investigadopedia"
fecha_limite:
actualizado: 2026-10-06
url_produccion: "https://investigadopedia.evegat.cl"
repositorio: "https://github.com/evegat/investigadopedia"
referencia_externa: "2 - Project/EDI001 - Investigadopedia/PRD Investigadopedia.md"
---

# Investigadopedia

Proyecto de metodología aplicada sobre el uso responsable de Inteligencia Artificial Generativa en la investigación científica y la gestión del conocimiento académico.

Giro de enfoque 2026-06-15: Investigadopedia pasa a operar también como una biblioteca curada sobre investigar. La prioridad inmediata no es solo construir una app, sino levantar, acuñar, traducir y ordenar contenidos, herramientas, flujos y criterios sobre investigación, llevándolos a un lenguaje hispanoamericano claro, exigente y metodológicamente útil.

Registro operativo: [[Registro de Iniciativas]]
Hoja de ruta y backlog: [[Features y Hoja de Ruta - Investigadopedia]]
Línea de curaduría: [[Curaduria de Investigacion Hispanohablante]]
Avance observatorio: [[Observatorio IA para Investigar - Formulacion y Hoja de Ruta]]
Paper vivo: [[Paper - Investigadopedia Observatorio]]
Corpus inicial: [[Corpus inicial - apoyos IA para investigar]]
Financiamiento y revisión experta: [[Analisis experto y financiamiento]]

---

## Enfoque actual

Investigadopedia debe curar todo contenido relevante sobre investigar:

- herramientas y agentes de investigación asistida por IA;
- flujos de revisión bibliográfica, formulación, método, datos, análisis, escritura y auditoría;
- conceptos que convenga acuñar en español hispanoamericano;
- riesgos metodológicos y resguardos prácticos;
- patrones reutilizables para prompts, talleres, fichas, artículos y prototipos.

La curaduría no debe ser traducción literal. Cada fuente se procesa en cuatro capas:

1. **Qué dice la fuente**: hecho observado, con enlace o archivo.
2. **Qué patrón aporta**: capacidad, flujo, criterio o riesgo reutilizable.
3. **Cómo se dice en lenguaje hispano**: traducción conceptual, no calco.
4. **Cómo entra a Investigadopedia**: benchmark, módulo, prompt, ficha, taller o descarte.

## Fuente semilla

- [[Registro de Iniciativas#2026-06-15 - Feynman CLI|Feynman CLI]]: agente open source de investigación. Sirve como primer benchmark para separar búsqueda, revisión, auditoría, escritura y verificación.

## Estudio de Mercado y Soluciones Existentes (Buy vs. Build)
*   **Asistentes de Búsqueda y Síntesis (Elicit, Consensus, SciSpace, ChatPDF)**: Enfocadas en automatizar la búsqueda bibliográfica, extraer resúmenes de PDFs o redactar fragmentos de texto. Tienen el riesgo de inducir alucinaciones, dependencia del usuario y pérdida de juicio metodológico experto.
*   **Investigadopedia (Build)**: Se diferencia por proponer una infraestructura de *razonamiento y auditoría metodológica*. La IA no redacta el paper; opera como un **interlocutor mayéutico** exigente que cuestiona las debilidades del diseño, audita la coherencia entre el problema, la pregunta, el método y los datos, e impone resguardos de trazabilidad.

---

## Definición de Arquitectura del MVP
*   **Interfaz de Usuario (Frontend)**: Aplicación SPA web estática (HTML/CSS/JS nativo existente en `app-demo/index.html`) de 3 pantallas:
    1.  **Pantalla 1: Formulación de la Idea**: El usuario ingresa su problema e ideas vagas.
    2.  **Pantalla 2: Interlocución Mayéutica**: Chat interactivo con el agente experto que interroga y exige justificaciones lógicas.
    3.  **Pantalla 3: Ficha Metodológica Exportable**: Generación de un reporte estructurado de coherencia, checklists de sesgos y registro de trazabilidad de cambios en Markdown.
*   **Backend / Orquestación IA**: Prompt maestro de sistema (diseñado en `System Prompt - Tutor Mayeutico.md`) ejecutado a través de la API de OpenRouter (preferencia Claude-3.5-Sonnet por sus excepcionales habilidades de razonamiento lógico y estructuración).

---

## Plan de Acción y Hoja de Ruta
*   **Fase 1: Feedback del PRD (1 semana)**: Consolidar comentarios de Valentina Cariaga y cerrar el documento de requisitos del MVP.
*   **Fase 2: Conexión API y Prototipo Web (2 semanas)**: Implementar la llamada a OpenRouter en el prototipo local de `app-demo` y validar el comportamiento del Tutor Mayéutico.
*   **Fase 3: Diseño de Ejercicios Prácticos del Taller (2 semanas)**: Diseñar los 3 ejercicios del taller (formulación, coherencia y auditoría) para empaquetamiento comercial.

---

## Ficha Ejecutiva para Reuniones (Offline 2-Minutos)

*   **¿Qué es?**: Arnés integral de investigación científica y toolkit agéntico distribuible (Core v1.0.0, Python estándar, zero-dependencies). Resuelve la recolección desinsesgada de literatura iberoamericana (SciELO + Redalyc vía OpenAlex/ISSN), el cribado semántico acelerado con TypeSafe Jev (System 1 RLCD) y la vigilancia epistemológica estricta (Hecho vs Inferencia vs Brecha).
*   **Problema que resuelve**: Los buscadores comerciales (Scopus/Web of Science) sesgan por idioma inglés y conteo de citas; mientras que SciELO y Redalyc no tienen APIs de búsqueda por palabras clave viables. Además, el uso ingenuo de LLMs introduce alucinaciones y confusión entre hechos empíricos y conjeturas.
*   **Capacidades paquetizadas (Core v1.0.0)**:
    1.  *Harvest*: Búsqueda booleana con abstracts reconstruidos en SciELO (2.274 revistas) y Redalyc (~371k obras).
    2.  *Dedup & Partition*: Deduplicación atómica no-Latin safe y separación física entre literatura revisada por pares (`corpus_academic.jsonl`) y literatura gris (`corpus_grey.jsonl`).
    3.  *Screening Jev*: Clasificación masiva de abstracts a $0.042/1M tokens (<300ms) con fallback heurístico determinista.
    4.  *Vigilancia Epistemológica*: Auditoría automatizada de manuscritos para garantizar distinción categórica Hecho/Inferencia/Supuesto.
    5.  *Reporte PRISMA 2020*: Generación instantánea de diagramas de flujo Mermaid y tablas de exclusión reproducibles.
    6.  *Dónde Publicar y Catálogo de Habilidades (Estilo aitmpl)*: Recomendador de revistas Acceso Abierto Diamante (SciELO, Redalyc, Latindex 2.0), extracción de pares revisores vía OpenAlex con privacidad en el cliente, y catálogo interactivo de habilidades, prompts tutores y observatorios abiertos con copia de un clic.
*   **Estado actual**: En producción en `https://investigadopedia.evegat.cl` (Coolify VPS + Cloudflare SSL). Repositorio oficial sincronizado en `evegat/investigadopedia`. Suite completa de 22 pruebas unitarias verdes bajo arnés MyWorld v1. Listo para uso de terceros.

---

## Próximas acciones

- [x] Formular Investigadopedia como observatorio curador open source de apoyos IA para investigar. <!-- myworld-task:2adbea25a9 -->
- [x] Crear corpus inicial de herramientas y casos por etapa de investigación. <!-- myworld-task:2b6ca028a1 -->
- [x] Generar borrador de paper para el observatorio. <!-- myworld-task:5e359e32a1 -->
- [x] Crear prototipo local full stack mock en `app-demo/observatorio`. <!-- myworld-task:2ea816c3a5 -->
- [x] Preparar análisis experto simulado, rutas de financiamiento y destinos de publicación. <!-- myworld-task:1e7ce1c7ce -->
- [x] Paquetizar Investigadopedia Core v1.0.0 autónomo (`harvest`, `dedup`, `screen`, `epistemic`, `prisma`). <!-- myworld-task:c01e1001a1 -->
- [x] Publicar router agéntico unificado en `.agents/skills/investigadopedia/SKILL.md`. <!-- myworld-task:c01e1002a2 -->
- [x] Implementar módulo Dónde Publicar y Catálogo de Habilidades/Repositorios estilo aitmpl en la web pública. <!-- myworld-task:c01e1004a4 -->
- [ ] Incorporar conectores adicionales de literatura (arXiv preprint harvester y Crossref DOI resolver directo). <!-- myworld-task:c01e1003a3 -->

