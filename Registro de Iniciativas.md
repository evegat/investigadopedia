---
tipo: registro
estado: activo
prioridad_categoria: reputacion
activo_legado: conocimiento
actualizado: 2026-06-15
referencia_externa:
---

# Registro de Iniciativas - Investigadopedia

Espacio para registrar herramientas, repositorios, flujos, ideas de producto y oportunidades que puedan alimentar Investigadopedia sin convertirlas automaticamente en decisiones de roadmap.

Desde 2026-06-15 este registro alimenta una segunda capa del proyecto: [[Curaduria de Investigacion Hispanohablante]]. La prioridad es levantar contenidos sobre investigar, acunar conceptos utiles y pasarlos a lenguaje hispanoamericano antes de decidir si entran a producto, taller, articulo o prompt.

## Criterio de registro

- **Hecho observado**: informacion disponible en la fuente revisada.
- **Lectura para Investigadopedia**: inferencia propia sobre como podria servir al proyecto.
- **Traduccion hispana**: forma recomendada de nombrar el patron en espanol academico-practico.
- **Decision pendiente**: accion minima para validar si se incorpora, se descarta o queda como referencia.

---

## 2026-06-15 - Feynman CLI

**Fuente:** [companion-inc/feynman](https://github.com/companion-inc/feynman)  
**Tipo:** herramienta / agente de investigacion open source  
**Estado:** por evaluar  
**Relacion con Investigadopedia:** benchmark funcional y posible referencia de capacidades, no sustituto del MVP.

### Hecho observado

Feynman se presenta como un agente de investigacion open source orientado a buscar papers y web, producir briefs citados, ejecutar revisiones de literatura, comparar fuentes, auditar claims de papers contra codebases, replicar experimentos y proponer recetas de entrenamiento ML.

Incluye comandos o flujos como:

- `deepresearch`: investigacion multiagente con sintesis y verificacion.
- `lit`: revision de literatura con consensos, desacuerdos y preguntas abiertas.
- `review`: revision simulada por pares con severidad y plan de revision.
- `audit`: comparacion entre claims de un paper y codigo publico.
- `replicate`: replicacion de experimentos en GPU local o cloud.
- `recipe`: recetas implementables desde papers, datasets, documentacion y codigo.

Tambien declara agentes internos de investigacion, revision, escritura y verificacion, ademas de integraciones con AlphaXiv, Hugging Face Hub, Docker, busqueda web, preview, Modal y RunPod. El clipping menciona instalacion como app terminal y una modalidad "skills only" para Codex.

### Lectura para Investigadopedia

Feynman parece mas cercano a una infraestructura de investigacion automatizada y revision tecnica que a un tutor metodologico mayeutico. Puede servir como referencia para:

- separar agentes por funcion: investigador, revisor, escritor, verificador;
- disenar comandos o modos explicitos para literatura, auditoria, comparacion y borradores;
- estudiar como empaquetar skills reutilizables para Codex;
- observar mecanismos de verificacion de fuentes y enlaces;
- contrastar la diferencia entre "investigar por el usuario" y "exigir justificacion metodologica al usuario".

### Traduccion hispana

- `deepresearch` -> investigacion profunda asistida.
- `lit` -> revision de literatura.
- `review` -> revision simulada por pares.
- `audit` -> auditoria de coherencia o auditoria de evidencia, segun el objeto.
- `Verifier` -> verificador de fuentes y trazabilidad.

Regla editorial: no traducir Feynman como promesa de autonomia investigativa. En Investigadopedia, cada modo debe responder a una pregunta metodologica: que evidencia hay, que metodo calza, que afirmacion se puede sostener y que decision humana queda registrada.

Para Investigadopedia, la oportunidad no es copiar el producto, sino aislar patrones utiles:

- modo `lit` como insumo para revision bibliografica asistida;
- modo `review` como antecedente para auditoria metodologica;
- modo `audit` como analogia para contrastar afirmaciones, metodo, datos y evidencia;
- agente `Verifier` como referencia para una capa de trazabilidad.

### Riesgos o limites

- Podria reforzar una logica de automatizacion que Investigadopedia quiere evitar si el usuario delega juicio experto.
- La ficha proviene de un clipping; no se verifico en vivo el estado actual del repositorio, releases ni documentacion.
- Varias capacidades declaradas dependen de servicios externos, credenciales o compute que no necesariamente son parte del MVP.

### Decision pendiente

- [ ] Revisar si conviene instalar solo las skills de Feynman en Codex para evaluar sus patrones sin adoptar la app completa.
- [ ] Probar un caso minimo: una revision `lit` o `review` sobre un tema de Investigadopedia.
- [ ] Extraer 3 patrones reutilizables para el Tutor Mayeutico: verificacion, auditoria y separacion de roles.
- [ ] Decidir si queda como benchmark externo, integracion futura o referencia descartada.

---

## 2026-09-29 - Regional Literature Harvest (SciELO & Redalyc via OpenAlex)

**Fuente:** Ian Scott Kinney (2026), *Regional Literature Harvest: Keyword search over SciELO and Redalyc via the OpenAlex identifier universe* (Technical white paper v1.1.2)  
**Tipo:** arquitectura de búsqueda / toolkit en Python estándar / método bibliográfico  
**Estado:** adoptado (Estrategia Híbrida Bifásica validada por TypeSafe Jev)  
**Relación con Investigadopedia:** infraestructura desacoplada para mitigar sesgo de citación anglocéntrico en revisión de literatura, proveyendo acceso booleano a SciELO (~900k) y Redalyc (~371k).

### Hecho observado

SciELO y Redalyc representan los dos mayores reservorios de acceso abierto para la ciencia iberoamericana, pero carecen de APIs públicas funcionales de búsqueda por palabras clave:
- SciELO ofrece solo `ArticleMeta` (búsqueda unitaria por identificador) y bloquea clientes automáticos en su buscador web con HTTP 403.
- Redalyc no es miembro de Crossref y su endpoint OAI-PMH está roto.

El autor propone la técnica de *la ruta del universo de identificadores* (*identifier-universe route*):
1. No hace web scraping de los portales.
2. Consulta la API abierta de OpenAlex.
3. Para Redalyc, filtra por sus dos identificadores de fuente de repositorio (`S4377196100` y `S4306402163`), habilitando búsqueda booleana directa sobre ~371.000 obras con resúmenes reconstruidos.
4. Para SciELO, toma el registro de 2.274 revistas (24 colecciones) y acota la búsqueda a ese universo de ISSNs, asegurando que las obras regionales compitan exclusivamente entre sí, anulando el sesgo algorítmico de citación en inglés (*citation-ranking bias*).
5. Implementado en Python 3.8+ estándar (cero dependencias externas), con falla ruidosa (*fail loud*, sin falsos ceros), checkpoints atómicos en JSONL y deduplicación por DOI/título.

### Lectura para Investigadopedia

1. **Aporte epistémico al Observatorio/Paper:** Resuelve metodológicamente una crítica central a la IA en revisión de literatura: la invisibilidad de la producción del sur global y el sesgo algorítmico de los motores comerciales anglosajones.
2. **Capacidad de fuego desacoplada:** Permite a los agentes de investigación y a Eduardo recolectar evidencia científica regional para alimentar tesis, talleres o revisiones sin recargar el MVP web.
3. **Calibración Jev System 1 (2026-09-29):** La simulación de 4 escenarios determinó que la *Estrategia Híbrida Bifásica* (ESC_D, P=0.65) es superior tanto a la mera curaduría pasiva (P=0.46) como al acoplamiento directo al frontend web (P=0.54).

### Traducción hispana

- *Identifier-universe route* -> Ruta por universo de identificadores.
- *Citation-ranking bias* -> Sesgo por ordenación de citas.
- *Fail loud* -> Fallo explícito (tolerancia cero a falsos ceros).
- *Query battery* -> Batería sistemática de consultas.
- *Abstract inverted index reconstruction* -> Reconstrucción de resumen continuo.

### Riesgos o límites

- OpenAlex indexa lo que tiene catalogado de cada fuente; si una revista regional reciente no está vinculada en OpenAlex, debe recurrirse a enumeración directa por `ArticleMeta`.
- El límite de caracteres en URLs exige paginación y segmentación (*chunking*) al consultar grandes listas de ISSNs.

### Decisiones tomadas y ejecutadas

- [x] Evaluados escenarios con TypeSafe Jev System 1 RLCD (Memoria Engram #459).
- [x] Creado skill local desacoplado en `3 - SistemaMyworld/Skills/investigadopedia/regional-literature-harvest`.
- [x] Verificada ejecución del script `regional_harvest.py` con descarga exitosa de corpus en formato JSONL atómico.
- [ ] Incorporar el patrón metodológico en el borrador del Paper vivo de Investigadopedia.

