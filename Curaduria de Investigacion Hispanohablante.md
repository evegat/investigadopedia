---
tipo: recurso
estado: activo
prioridad_categoria: reputacion
activo_legado: conocimiento
actualizado: 2026-06-15
referencia_externa: "https://github.com/companion-inc/feynman"
---

# Curaduria de Investigacion Hispanohablante

## Proposito

Convertir Investigadopedia en una biblioteca viva para investigar mejor con IA: levantar fuentes, curarlas, acunar conceptos utiles y pasarlos a un lenguaje hispanoamericano claro, sobrio y metodologicamente exigente.

La unidad de trabajo no es solo "herramienta encontrada". Es una ficha curada que traduzca una practica de investigacion a criterios accionables para estudiantes, tesistas, academicos, consultores y equipos publicos o tecnicos.

## Criterio editorial

- No copiar marketing de herramientas.
- No traducir literalmente comandos, claims o nombres si pierden sentido local.
- Separar hecho observado, lectura propia y decision pendiente.
- Mantener trazabilidad hacia la fuente original.
- Marcar capacidades no verificadas o dependientes de servicios externos.
- Preferir lenguaje academico-practico: claro, exigente, usable en Chile y America Latina.

## Pipeline de curaduria

1. **Captura**
   - Fuente original.
   - Tipo: paper, herramienta, prompt, curso, guia, repositorio, caso, protocolo.
   - Fecha de revision.
   - Enlace, archivo o evidencia local.

2. **Extraccion**
   - Que problema de investigacion aborda.
   - Que flujo propone.
   - Que roles separa.
   - Que salidas produce.
   - Que verificaciones exige.
   - Que riesgos abre.

3. **Traduccion conceptual**
   - Termino original.
   - Traduccion literal, si aplica.
   - Traduccion hispana recomendada.
   - Justificacion de la eleccion.
   - Ejemplo de uso.

4. **Adaptacion a Investigadopedia**
   - Entra como benchmark, modulo, ficha, prompt, taller, articulo o descarte.
   - Riesgo de delegacion cognitiva.
   - Resguardo metodologico requerido.
   - Proximo experimento minimo.

## Taxonomia inicial

| Area | Pregunta guia | Salida curada |
|---|---|---|
| Formulacion | Que hace investigable una intuicion? | ficha de problema, pregunta y alcance |
| Literatura | Como se revisa evidencia sin inventar fuentes? | matriz de literatura y vacios |
| Metodo | Que metodo responde la pregunta? | justificacion metodologica |
| Datos | Que evidencia permite sostener que afirmacion? | matriz objetivo-dato-analisis |
| Analisis | Que inferencias son legitimas? | limites y tecnicas atingentes |
| Escritura | Como escribir sin delegar criterio? | pauta de argumento y atribucion |
| Auditoria | Que puede estar mal alineado? | checklist de coherencia |
| Trazabilidad | Que decisiones deben quedar registradas? | log de cambios metodologicos |

## Ficha fuente - Feynman CLI

**Fuente:** [companion-inc/feynman](https://github.com/companion-inc/feynman)  
**Fecha de revision:** 2026-06-15  
**Tipo:** agente open source de investigacion  
**Estado en Investigadopedia:** fuente semilla / benchmark externo

### Hecho observado

El repositorio se presenta como un agente de investigacion open source. Su README describe instalacion para Windows, macOS y Linux, una modalidad "skills only" para Codex y workflows como investigacion profunda, revision de literatura, revision simulada, auditoria de paper contra codigo, replicacion, comparacion de fuentes, redaccion y monitoreo.

Tambien declara agentes internos separados por funcion: investigacion, revision, escritura y verificacion. Las herramientas mencionadas incluyen busqueda academica/web, AlphaXiv, Hugging Face Hub, Docker, preview y opciones de compute como Modal o RunPod.

### Lectura para Investigadopedia

Feynman no debe leerse como modelo a copiar. Su valor esta en mostrar una arquitectura de roles y flujos para investigar con IA:

- buscar evidencia;
- sintetizar literatura;
- comparar desacuerdos;
- revisar claims;
- verificar enlaces y citas;
- generar borradores desde hallazgos.

Investigadopedia puede tomar esa separacion de funciones, pero debe conservar su diferencia central: no investigar en reemplazo del usuario, sino ayudar a investigar con trazabilidad, justificacion y conciencia metodologica.

### Traduccion hispana recomendada

| Original | Traduccion util | Nota editorial |
|---|---|---|
| deep research | investigacion profunda asistida | Evitar venderlo como autonomia total. |
| literature review | revision de literatura | Mantener termino academico estandar. |
| simulated peer review | revision simulada por pares | Debe declararse como simulacion, no validacion real. |
| audit | auditoria de coherencia / auditoria de evidencia | En Investigadopedia conviene orientar a metodo, datos y afirmaciones. |
| verifier | verificador de fuentes y trazabilidad | No basta con "verificador"; debe decir que verifica. |
| recipe | receta implementable / pauta replicable | Usar solo cuando haya pasos, datos y criterios de validacion. |

### Patrones reutilizables

- Separar agentes por etapa: investigador, revisor, escritor, verificador.
- Convertir modos de trabajo en comandos o rutas explicitas.
- Exigir outputs citados y verificables.
- Mantener una capa de auditoria independiente de la capa de escritura.
- Distinguir busqueda de evidencia, sintesis y decision metodologica.

### Riesgos

- Puede reforzar la idea de que investigar es delegable a un agente.
- Algunas capacidades dependen de servicios externos, credenciales o compute.
- La verificacion tecnica de enlaces no equivale a validacion metodologica.
- La redaccion automatizada puede homogeneizar el argumento si no hay criterio humano.

### Adaptacion inicial

- Usar Feynman como benchmark, no como nucleo del producto.
- Probar sus "skills only" solo si aporta patrones concretos a Codex.
- Extraer una ficha comparativa: Feynman investiga; Investigadopedia exige justificar como se investiga.
- Convertir `review`, `audit` y `verifier` en tres modulos conceptuales de Investigadopedia:
  - revision metodologica;
  - auditoria de coherencia;
  - trazabilidad de fuentes, datos y decisiones.

---

## Ficha 2: Pauta de Arbitraje Editorial y Revisión Crítica de Papers (Dra. Naureen Aleem, 2026)

### 1. Qué dice la fuente
- **Fuente:** Dra. Naureen Aleem (Editora en Jefe académica y especialista en publicación científica).
- **Publicación:** *How to Review a Research Paper* (LinkedIn Pulse, 2026).
- **Contenido:** Guía operativa para revisores y editores que desglosa el arbitraje de manuscritos en 7 preguntas estructuradas:
  1. *Significance:* ¿Aborda un problema de investigación importante? ¿Quién se beneficia? ¿Aporta a teoría o política pública?
  2. *Literature Gap:* ¿Identifica con precisión la brecha de conocimiento que viene a llenar?
  3. *Theoretical Framework:* ¿El marco conceptual articula coherentemente el diseño?
  4. *Methodology:* ¿El diseño empírico/muestral es replicable y adecuado?
  5. *Findings:* ¿Los hallazgos se sustentan estrictamente en la evidencia sin extrapolar?
  6. *Discussion & Limitations:* ¿Contrasta con la literatura y reconoce sus propias limitaciones con honestidad?
  7. *Ethics & Referencing:* ¿Citas verificables, datos abiertos y ausencia de conflictos éticos?

### 2. Qué patrón aporta
- **Evaluación por Rúbrica Multidimensional:** Desarma la crítica vaga de un manuscrito ("está bueno" o "le falta") en un checklist de 7 dimensiones con dictamen claro (`Aceptar con cambios menores`, `Requiere revisión mayor`, `Rechazar por brechas estructurales`).
- **Anticipación del Revisor 2:** Permite simular localmente las objeciones que un revisor anónimo formulará antes de someter el paper a la revista.

### 3. Cómo se traduce a lenguaje hispano
- *Significance* -> **Relevancia e Impacto Público/Teórico** (no "significancia", que en español suele confundirse con significancia estadística).
- *Literature Gap* -> **Brecha del Estado del Arte**.
- *Simulated Peer Review* -> **Arbitraje Editorial Simulado**.
- *Desk Reject Pre-check* -> **Filtro Pre-Editorial de Mesa**.

### 4. Cómo entra a Investigadopedia
- Implementado en el core autónomo: `core/investigadopedia/epistemic/peer_review.py`.
- Expuesto en CLI: `investigadopedia review-manuscript --file manuscrito.md --out reporte_revision.md`.
- Conectado a la Cartera de Publicaciones (`PUB###`): Gate pre-submission para auditar papers antes de la postulación formal a revistas indexadas.

---

## Ficha 3: Cosecha de Literatura Regional SciELO y Redalyc (Ian Scott Kinney, 2026)

### 1. Qué dice la fuente
- **Fuente:** Ian Scott Kinney (2026).
- **Publicación:** *Regional Literature Harvest: Keyword search over SciELO and Redalyc via the OpenAlex identifier universe* (Technical white paper v1.1.2).
- **Contenido:** Especificación de arquitectura y toolkit para recuperar literatura científica en acceso abierto en América Latina, el Caribe y la Península Ibérica. Supera la ausencia de APIs de búsqueda por palabras clave en SciELO y Redalyc apoyándose en la API abierta de OpenAlex acotada al universo de identificadores (2.274 ISSNs de SciELO y 2 fuentes de repositorio de Redalyc). Implementado exclusivamente en Python estándar (sin dependencias de terceros), con falla explícita (*fail loud*), resúmenes reconstruidos y checkpoints atómicos en JSONL.

### 2. Qué patrón aporta
- **Ruta por universo de identificadores (*identifier-universe route*):** Neutralización sistemática del sesgo de citación anglocéntrico (*citation-ranking bias*). Al restringir la búsqueda a un universo cerrado de revistas iberoamericanas, la literatura regional compite únicamente contra pares regionales en lugar de quedar sepultada por la cola larga anglosajona.
- **Tolerancia cero a falsos ceros (*fail loud*):** Si la consulta falla o se satura la cuota de red, el sistema reporta error explícito no-cero en lugar de falsear un "0 resultados encontrados".
- **Reconstrucción determinista de resúmenes:** Reensambla el índice invertido de palabras de OpenAlex a texto continuo sin requerir LLMs ni inferencia generativa.

### 3. Cómo se traduce a lenguaje hispano
- *Identifier-universe route* -> **Ruta por universo de identificadores**.
- *Citation-ranking bias* -> **Sesgo por ordenación de citas**.
- *Fail loud* -> **Fallo explícito (rechazo a falsos ceros)**.
- *Query battery* -> **Batería sistemática de consultas**.
- *Atomic checkpoint* -> **Punto de control atómico**.

### 4. Cómo entra a Investigadopedia
- **Decisión estratégica Jev (System 1 RLCD, 2026-09-29):** Adoptada *Estrategia Híbrida Bifásica* ($P=0,65$, impacto transformador práctico).
- **Skill operativo local:** Desplegado en `3 - SistemaMyworld/Skills/investigadopedia/regional-literature-harvest` con script `scripts/regional_harvest.py` en Python stdlib puro.
- **Aporte al Paper vivo / Observatorio:** Incorporar la técnica como caso de estudio metodológico de auditoría bibliográfica y mitigación del sesgo anglocéntrico en revisiones sistemáticas asistidas por IA.

---

## Backlog

- [x] Curar pauta de arbitraje editorial de Dra. Naureen Aleem (2026).
- [x] Curar y empaquetar Regional Literature Harvest (SciELO/Redalyc vía OpenAlex, Kinney 2026).
- [ ] Crear plantilla unica de ficha curada.
- [ ] Curar Feynman en una ficha comparativa contra el PRD actual.
- [ ] Levantar 10 fuentes iniciales sobre investigacion asistida por IA.
- [ ] Acunar un glosario inicial de terminos hispanoamericanos.
- [ ] Definir cuales contenidos entran a taller, articulo, prompt y app.
- [ ] Separar biblioteca de contenidos de roadmap de producto.

