# Créditos y Referencias de Inspiración

Investigadopedia Core integra y adapta patrones, metodologías y arquitecturas desarrolladas por investigadores, iniciativas de ciencia abierta y proyectos pioneros de automatización de la investigación:

## 1. Cosecha y Minería de Literatura Regional
*   **Regional Literature Harvest (v1.1.2, 2026)** — *Ian Scott Kinney (Journal Revisions)*:
    - Técnica de consulta acotada al universo de 2.274 ISSNs de SciELO y los IDs de repositorio de Redalyc (`S4377196100` / `S4306402163`) sobre OpenAlex.
    - Reconstrucción de abstracts desde índices invertidos.
    - Principios de ingeniería: política de *Fallo Ruidoso* (*Fail Loud*, jamás reportar 0 silencioso ante caídas de API), checkpoints atómicos y preservación de alfabetos no-latinos (cirílico, CJK).

## 2. Cribado y Selección Activa de Literatura
*   **ASReview Lab** — *Universidad de Utrecht*:
    - Paradigma de cribado acelerado mediante aprendizaje activo y evaluación predictiva de relevancia según criterios de inclusión/exclusión.
*   **TypeSafe AI (Jev / System 1 RLCD)** — *Diogo Almeida*:
    - Arquitectura no-autoregresiva entrenada con Reinforcement Learning for Calibrated Decisions (RLCD) para evaluación semántica tipada, masiva y determinista de abstracts.

## 3. Síntesis Basada en Evidencia y Trazabilidad
*   **PaperQA / PaperQA2** — *FutureHouse (Andrew White et al.)*:
    - Principios de generación fundamentada en texto (grounding) y anclaje estricto de afirmaciones a citas textuales verificables, eliminando alucinaciones generativas.
*   **Vigilancia Epistemológica MyWorld**:
    - Separación categórica e irrenunciable entre *Hecho Observado*, *Inferencia Fundada* y *Supuesto / Brecha*.

## 4. Fuentes de Datos Abiertos e Infraestructura Global
*   **OpenAlex** — *OurResearch*:
    - Grafo de conocimiento científico abierto sobre más de 250 millones de obras académicas.
*   **Crossref**:
    - Infraestructura de registro de metadatos, resolución de identificadores persistentes (DOIs) y verificación bibliográfica.

## 5. Estándares Metodológicos
*   **PRISMA 2020 Statement** — *Page MJ et al.*:
    - Guías y directrices internacionales para la publicación y reporte transparente de revisiones sistemáticas y metasíntesis.

## 6. Arbitraje Editorial y Revisión por Pares (Peer Review)
*   **Directrices de Revisión de Manuscritos Científicos (2026)** — *Dra. Naureen Aleem*:
    - Rúbrica editorial de evaluación en 7 dimensiones críticas: relevancia e impacto social/teórico, detección de brecha en el estado del arte, coherencia del marco conceptual, replicabilidad metodológica, consistencia del análisis empírico, discusión honesta de limitaciones y trazabilidad bibliográfica ética.
