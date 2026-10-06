---
tipo: paper
estado: borrador
prioridad_categoria: reputacion
activo_legado: conocimiento
actualizado: 2026-06-15
---

# Investigadopedia Observatorio: curaduria abierta y auditoria metodologica de apoyos IA para investigar

## Resumen

La proliferacion de herramientas de inteligencia artificial para investigacion academica ha creado una paradoja practica: existen mas apoyos que nunca para buscar literatura, resumir papers, producir codigo, redactar borradores y revisar afirmaciones, pero los investigadores enfrentan mayores riesgos de delegacion cognitiva, referencias inventadas, perdida de trazabilidad y desalineacion metodologica. Este articulo propone Investigadopedia Observatorio, una infraestructura abierta de curaduria y auditoria metodologica para ordenar apoyos IA por etapa de investigacion. A diferencia de los asistentes que automatizan la produccion de resultados, el observatorio busca ayudar a decidir que herramienta usar, para que etapa, con que evidencia, bajo que resguardos y con que validacion humana. Se presenta una taxonomia por etapas, un corpus inicial de herramientas y literatura, un prototipo funcional con chat auditor y una agenda de evaluacion experta. La contribucion central es un modelo de "friccion metodologica positiva": introducir deliberadamente controles de justificacion antes de permitir que la IA acelere escritura, sintesis o analisis.

## 1. Introduccion

La IA generativa entro rapidamente en practicas de investigacion: formulacion de preguntas, revision de literatura, lectura de PDFs, programacion, analisis, escritura, traduccion y revision. La promesa es evidente: reducir tiempos, ampliar exploracion y mejorar productividad. El riesgo tambien: confundir fluidez textual con validez metodologica.

El problema no es solo que la IA pueda alucinar citas. Es que puede hacer avanzar una investigacion mal formulada con apariencia de rigor. Un investigador puede obtener un marco teorico prolijo antes de haber delimitado pregunta, unidad de analisis, metodo, datos y limites de inferencia.

Investigadopedia parte de una regla: la pregunta manda, los objetivos obedecen, el metodo responde y los datos sostienen. Desde esa regla, este articulo propone pasar de una app de tutor mayeutico a un observatorio curador de apoyos IA para investigar como bien publico open source.

## 2. Antecedentes

El mercado ya ofrece herramientas relevantes:

- Elicit declara soporte para acelerar etapas de revision sistematica, incluyendo protocolo, busqueda, screening, extraccion y sintesis.
- Consensus se presenta como buscador academico con IA sobre literatura revisada por pares.
- SciSpace ofrece revision de literatura y conversacion con PDFs.
- ResearchRabbit y Litmaps apoyan mapeo de literatura y redes de citacion.
- Feynman se presenta como agente open source capaz de buscar papers/web/repos, redactar, revisar y verificar fuentes mediante roles separados.

La evidencia academica disponible sugiere cautela. Tosi (2025) comparo revisiones de literatura generadas con IA frente a revisiones humanas y encontro eficiencia potencial, pero tambien problemas de recall, sesgo hacia papers muy citados y analisis critico limitado. Adel y Alani (2025) reportan reducciones de carga de trabajo, pero precision variable y tasas altas de alucinacion en tareas de revision. Chelli et al. (2024) muestran baja precision y recall en referencias para revisiones sistematicas, con tasas importantes de referencias alucinadas. Resnik y Hosseini (2026) advierten que las citas alucinadas pueden adquirir gravedad etica especial cuando las referencias funcionan como datos de una revision. Templin et al. (2024) sintetizan desafios recurrentes: sesgo, privacidad, alucinacion, sobredependencia, ataques de prompt y cumplimiento regulatorio.

## 3. Problema de investigacion

La pregunta que organiza este trabajo es:

> Como disenar una infraestructura abierta que ayude a investigadores a usar apoyos IA por etapa de investigacion sin delegar juicio metodologico, perder trazabilidad ni producir falsa autoridad academica?

## 4. Tesis

La tesis es que los apoyos IA para investigar deben ser curados y auditados por etapa, no evaluados como herramientas genericas. La pregunta relevante no es "que herramienta es mejor", sino:

- para que etapa sirve;
- que evidencia procesa;
- que decision deja al humano;
- que riesgo introduce;
- que salida produce;
- que trazabilidad permite.

## 5. Metodo propuesto

Este borrador usa un enfoque de investigacion-disenno:

1. Revision exploratoria de herramientas y literatura sobre IA para investigacion.
2. Curaduria de fuentes mediante ficha comun: hecho observado, patron, traduccion hispana, riesgo, resguardo y decision.
3. Disenno de taxonomia por etapas de investigacion.
4. Prototipado de una app abierta con catalogo, chat auditor y exportacion.
5. Evaluacion experta simulada inicial, a reemplazar por entrevistas y revision por pares reales.

## 6. Taxonomia de apoyo IA por etapa

La taxonomia distingue siete etapas: formulacion, literatura, metodo, datos, analisis, escritura y auditoria. Cada etapa exige una separacion entre apoyo de IA y validacion humana. Esto evita que la herramienta sea evaluada por su capacidad generativa global y fuerza una pregunta metodologica: que decision se esta tomando y con que evidencia.

## 7. Prototipo

El prototipo implementado en `app-demo/observatorio` incluye:

- catalogo curado de herramientas;
- filtros por etapa;
- panel de evidencia y resguardos;
- chat auditor metodologico con respuestas mock reproducibles;
- endpoint local `/api/tools`;
- endpoint local `/api/audit`;
- exportacion Markdown de ficha de seleccion.

No usa claves externas ni envia datos a servicios remotos. Es una maqueta full stack local para mostrar flujo, no una integracion productiva con modelos.

## 8. Contribucion

La contribucion esperada es triple:

1. **Conceptual:** definir la friccion metodologica positiva como principio de disenno para IA en investigacion.
2. **Practica:** entregar un corpus curado y una app clonable para elegir apoyos IA por etapa.
3. **Academica:** proponer un marco evaluable para estudiar si la curaduria reduce delegacion cognitiva y mejora trazabilidad.

## 9. Limitaciones

- El corpus inicial no es exhaustivo.
- Las fichas combinan fuentes oficiales, literatura academica y lectura propia; no equivalen a benchmark tecnico completo.
- La evaluacion experta incluida por ahora es simulada, no reemplaza revision real.
- El prototipo usa backend mock y no integra modelos en vivo.

## 10. Agenda de investigacion

La siguiente etapa debe responder:

- Que criterios usan investigadores para elegir herramientas IA?
- La taxonomia por etapas mejora la seleccion responsable?
- El chat auditor reduce afirmaciones metodologicamente injustificadas?
- Que diferencias aparecen entre tesistas, investigadores senior y equipos aplicados?
- Que gobernanza necesita un observatorio abierto para no transformarse en lista comercial?

## Referencias iniciales verificadas

- Adel, A., & Alani, N. H. S. (2025). "Can generative AI reliably synthesise literature? exploring hallucination issues in ChatGPT". AI & SOCIETY, 40, 6799-6812. https://consensus.app/papers/can-generative-ai-reliably-synthesise-literature-adel-alani/cfffa97c738b5c15a81470a16fc331ea/
- Chelli, M., Descamps, J., Lavoue, V., Trojani, C., Azar, M., Deckert, M., Raynier, J., Clowez, G., Boileau, P., & Ruetsch-Chelli, C. (2024). "Hallucination Rates and Reference Accuracy of ChatGPT and Bard for Systematic Reviews: Comparative Analysis". Journal of Medical Internet Research, 26. https://consensus.app/papers/hallucination-rates-and-reference-accuracy-of-chatgpt-and-chelli-descamps/5cd8dd78481e561688e4712599e8078a/
- Resnik, D. B., & Hosseini, M. (2026). "Hallucinated citations produced by generative artificial intelligence may constitute research misconduct when citations function as data in scholarly papers". Accountability in Research. https://consensus.app/papers/hallucinated-citations-produced-by-generative-resnik-hosseini/d2e00fe9d2ba5434aa2ba50d57d3a471/
- Templin, T., Perez, M. W., Sylvia, S., Leek, J., & Sinnott-Armstrong, N. (2024). "Addressing 6 challenges in generative AI for digital health: A scoping review". PLOS Digital Health, 3. https://consensus.app/papers/addressing-6-challenges-in-generative-ai-for-digital-templin-perez/ccec3ad2a21e5b56bba59ff4329a10af/
- Tosi, D. (2025). "Comparing Generative AI Literature Reviews Versus Human-Led Systematic Literature Reviews: A Case Study on Big Data Research". IEEE Access, 13, 56210-56219. https://consensus.app/papers/comparing-generative-ai-literature-reviews-versus-tosi/82910bfaeec559db9ed3e2fac3a0ffac/

## Declaracion de uso de IA

Este borrador fue preparado con asistencia de Codex/ChatGPT para busqueda, sintesis, estructuracion y prototipado. Las fuentes, afirmaciones y referencias deben ser revisadas manualmente antes de cualquier envio editorial.

