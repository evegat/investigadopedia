---
tipo: recurso
estado: pausa
prioridad_categoria: reputacion
activo_legado: conocimiento
proximo_paso: "Recibir feedback de Vale y convertir este PRD en plan de MVP"
criterio_terminado: "PRD revisado por Vale, decisiones incorporadas y MVP definido"
fecha_limite:
actualizado: 2026-05-07
referencia_externa:
---

# PRD Borrador - Investigadopedia

## 1. Resumen

**Investigadopedia** es una app de acompanamiento metodologico para investigadores, academicos, tesistas y equipos profesionales que usan IA generativa en procesos de investigacion.

No busca escribir papers automaticamente. Busca ayudar al usuario a **pensar, formular, justificar, analizar, replantear y documentar mejor** una investigacion asistida por IA.

La app guia al usuario desde una idea vaga hasta una ficha de investigacion estructurada, disciplinariamente situada, metodologicamente coherente, con plan de analisis de datos, resguardos frente a dependencia/sesgo y control de cambios del diseno.

## 2. Problema

Hoy muchos investigadores usan IA generativa de forma informal:

- entran a ChatGPT con una idea vaga;
- conversan sin metodo;
- corrigen respuestas iterativamente;
- aceptan respuestas fluidas pero no verificadas;
- no separan exploracion, analisis, redaccion y validacion;
- no registran decisiones metodologicas;
- no controlan sesgos ni alucinaciones;
- no conectan bien pregunta, objetivos, metodo, datos y afirmaciones;
- no saben que cambia cuando replantean el diseno.

El problema no es solo tecnico. Es metodologico, disciplinar y epistemologico.

## 3. Tesis Del Producto

La IA generativa puede acelerar y enriquecer la investigacion si se usa como **infraestructura metodologica asistida**, no como reemplazo del investigador.

Investigadopedia debe funcionar como un interlocutor metodologico exigente:

> Todo lo que requiera justificacion debe ser justificado.

La app no debe reemplazar el juicio experto. Debe provocarlo, ordenarlo, exigirlo y dejar trazabilidad.

## 4. Usuario Objetivo

### Usuario Primario

- Investigadores.
- Academicos.
- Tesistas.
- Profesionales que producen estudios, informes, articulos o proyectos aplicados.

### Usuario Secundario

- Equipos de investigacion.
- Docentes que guian tesis.
- Instituciones que necesitan protocolos de uso responsable de IA.
- Consultores o equipos tecnicos que producen evidencia aplicada.

## 5. Casos De Uso

1. Convertir una idea vaga en una pregunta investigable.
2. Situar una investigacion en una disciplina o campo de conocimiento.
3. Explorar enfoques posibles desde distintas disciplinas.
4. Evaluar si el metodo es atingente al campo.
5. Construir objetivos, tesis, metodo y datos.
6. Auditar coherencia entre pregunta, objetivos, metodo, datos y analisis.
7. Disenar un plan de analisis de datos vinculado a los objetivos.
8. Definir procesamiento de datos.
9. Replantear el diseno cuando algo no calza.
10. Comparar cambios contra el plan original.
11. Auditar riesgos del uso de IA.
12. Registrar decisiones metodologicas.
13. Generar protocolo de uso responsable de IA.
14. Exportar ficha para articulo, tesis, informe, post o proyecto.

## 6. Objetivo Del MVP

Permitir que un usuario ingrese una idea vaga y obtenga una ficha estructurada con:

- tipo de producto;
- area tematica;
- disciplina principal;
- enfoques posibles;
- problema;
- pregunta;
- objetivos;
- tesis o hipotesis;
- metodo;
- datos disponibles y necesarios;
- plan de analisis;
- procesamiento de datos;
- auditoria de coherencia;
- control de cambios;
- riesgos;
- resguardos;
- proximos pasos.

## 7. No Objetivos Del MVP

El MVP no debe:

- escribir un paper completo automaticamente;
- prometer veracidad de fuentes;
- reemplazar revision experta;
- hacer revision bibliografica completa;
- conectarse todavia a bases academicas externas;
- gestionar equipos complejos;
- construir comunidad o red social;
- ejecutar analisis estadistico real en la primera version;
- producir conclusiones sin evidencia.

## 8. Flujo Principal

```text
Idea vaga
-> Tipo de producto
-> Area tematica / disciplina
-> Enfoques posibles
-> Problema
-> Pregunta
-> Objetivos
-> Tesis / hipotesis
-> Metodo
-> Datos: acceso y uso
-> Plan de analisis de datos
-> Procesamiento de datos
-> Auditoria de coherencia
-> Resultados esperados / limites
-> Uso de IA por etapa
-> Riesgos y resguardos
-> Iteracion / replanteamiento
-> Control de impacto de cambios
-> Auditoria final
-> Exportacion
```

## 9. Pantallas / Modulos MVP

### 1. Inicio

Frase:

> Disena investigaciones con IA sin delegar tu juicio metodologico.

Acciones:

- Iniciar investigacion.
- Auditar una idea.
- Revisar un borrador.
- Replantear diseno.
- Crear protocolo de uso de IA.

Para MVP se prioriza:

- Iniciar investigacion.
- Replantear diseno.

### 2. Idea Inicial

Campo:

> Describe tu idea, problema o intuicion inicial.

La app pregunta:

- Que quieres construir?
- Articulo academico?
- Tesis?
- Informe?
- Ensayo?
- Post?
- App?
- Proyecto aplicado?

Salida:

```markdown
## Tipo de producto
```

### 3. Area Tematica Y Disciplina

Preguntas:

- En que area tematica se situa tu investigacion?
- Desde que disciplina quieres mirar el problema?
- Hay mas de una disciplina involucrada?
- Que comunidad academica deberia reconocer este trabajo como valido?
- Que revista, congreso o publico podria recibirlo?

Salida:

```markdown
## Area tematica
## Disciplina principal
## Disciplinas secundarias
## Comunidad academica objetivo
```

### 4. Enfoques Posibles

La app propone aproximaciones alternativas.

Ejemplo:

```markdown
### Gestion publica
Foco: capacidades institucionales, implementacion, modernizacion.

### Derecho administrativo
Foco: legalidad, responsabilidad, datos personales, debido proceso.

### Estudios organizacionales
Foco: adopcion tecnologica, cultura institucional, cambio interno.

### Ciencia de datos
Foco: calidad de datos, automatizacion, evaluacion tecnica.
```

Salida:

```markdown
## Enfoques considerados
## Enfoque elegido
## Justificacion disciplinar
```

### 5. Problema

Preguntas:

- Cual es el fenomeno?
- A quien afecta?
- Que tension observas?
- Por que importa?
- Que no esta resuelto?

Salida:

```markdown
## Problema de investigacion
```

### 6. Pregunta

La pregunta es el eje del diseno.

La app debe revisar:

- claridad;
- delimitacion;
- unidad de analisis;
- viabilidad;
- disciplina;
- datos necesarios;
- metodo posible.

Salida:

```markdown
## Pregunta central
## Preguntas secundarias
```

### 7. Objetivos

La app separa pregunta y objetivos.

Preguntas:

- Cual es el objetivo general?
- El objetivo general responde directamente a la pregunta?
- Que objetivos especificos permiten responder la pregunta?
- Cada objetivo especifico es analitico y no solo una tarea?
- Cada objetivo tiene datos y metodo asociado?

Salida:

```markdown
## Objetivo general
## Objetivos especificos
```

### 8. Tesis O Hipotesis

Preguntas:

- Que sostienes?
- Que puedes afirmar con seguridad?
- Que todavia es hipotesis?
- Que evidencia necesitarias?

Salida:

```markdown
## Tesis o argumento central
## Hipotesis, si aplica
```

### 9. Metodo

Opciones:

- revision conceptual;
- revision sistematica;
- analisis documental;
- estudio de caso;
- entrevistas;
- encuesta;
- datos administrativos;
- analisis comparado;
- prototipo metodologico;
- ensayo metodologico;
- metodos mixtos.

La app debe revisar si el metodo calza con disciplina, pregunta y objetivos.

Salida:

```markdown
## Metodos atingentes al campo
## Metodo elegido
## Justificacion del metodo
```

### 10. Datos: Acceso Y Uso

La app pregunta:

- Que datos existen?
- Que datos faltan?
- Quien los tiene?
- Son publicos, privados, sensibles o personales?
- Son datos primarios o secundarios?
- Cual es la unidad de analisis?
- Cual es el nivel de agregacion?
- Que periodo cubren?
- Que sesgos de origen tienen?
- Que permisos o resguardos requieren?

Salida:

```markdown
## Datos disponibles
## Datos necesarios
## Fuente de datos
## Unidad de analisis
## Nivel de agregacion
## Calidad de datos
## Restricciones eticas o legales
```

### 11. Plan De Analisis De Datos

Pregunta central:

> Como se conectan los datos con los objetivos de investigacion?

Matriz:

```markdown
## Matriz objetivo-datos-analisis

| Objetivo | Datos necesarios | Variables/dimensiones | Tecnica de analisis | Resultado esperado |
|---|---|---|---|---|
```

La app debe detectar inconsistencias:

> Tu objetivo dice evaluar impacto, pero tus datos solo permiten describir percepciones.

### 12. Procesamiento De Datos

Incluye:

- limpieza;
- normalizacion;
- codificacion;
- anonimizacion;
- transformacion;
- union de bases;
- creacion de variables;
- tratamiento de valores perdidos;
- control de duplicados;
- validacion de consistencia;
- documentacion del procesamiento.

Salida:

```markdown
## Plan de procesamiento de datos

Fuente:
Unidad de analisis:
Pasos de limpieza:
Transformaciones:
Variables derivadas:
Criterios de exclusion:
Tratamiento de faltantes:
Resguardos eticos:
Output esperado:
```

### 13. Auditoria De Coherencia

La app debe verificar consistencia entre:

```text
tema
-> problema
-> pregunta
-> objetivo general
-> objetivos especificos
-> hipotesis/tesis
-> metodo
-> datos
-> analisis
-> afirmaciones posibles
-> producto final
```

Matriz:

```markdown
| Elemento | Formulacion | Revision de coherencia | Alerta |
|---|---|---|---|
| Problema | ... | Esta conectado con la pregunta? | ... |
| Pregunta | ... | Es clara, delimitada e investigable? | ... |
| Objetivo general | ... | Responde a la pregunta? | ... |
| Objetivo especifico 1 | ... | Aporta al objetivo general? | ... |
| Metodo | ... | Permite responder la pregunta? | ... |
| Datos | ... | Son suficientes para los objetivos? | ... |
| Analisis | ... | Produce evidencia para la tesis? | ... |
```

Salida:

```markdown
## Auditoria de coherencia
## Diagnostico general
## Ajustes recomendados
```

### 14. Resultados Esperados Y Limites

Preguntas:

- Que tipo de resultado esperas?
- Que afirmaciones permiten sostener los datos?
- Que afirmaciones no permiten sostener?
- Donde estan los limites de interpretacion?
- Que debe quedar como hipotesis o discusion?

Salida:

```markdown
## Resultados esperados
## Limites de interpretacion
## Que afirmaciones permiten los datos
## Que afirmaciones no permiten los datos
```

### 15. Uso De IA Por Etapa

La app separa etapas del proceso investigativo:

```text
Pregunta -> literatura -> metodo -> datos -> analisis -> escritura -> revision -> auditoria
```

Tabla:

| Etapa | Que puede hacer IA | Que valida humano | Riesgo |
|---|---|---|---|
| Pregunta | generar alternativas | pertinencia | amplitud |
| Literatura | ordenar temas | fuentes reales | referencias falsas |
| Metodo | comparar disenos | viabilidad | mala eleccion |
| Datos | sugerir estructura | calidad y acceso | sesgo |
| Analisis | proponer tecnicas | pertinencia | sobreafirmacion |
| Escritura | mejorar claridad | argumento | homogeneizacion |
| Auditoria | detectar vacios | decision final | falsa seguridad |

### 16. Riesgos Y Resguardos

Riesgos base:

- dependencia;
- sesgo;
- falsa autoridad;
- alucinaciones;
- perdida de trazabilidad;
- autoria difusa;
- homogeneizacion del pensamiento;
- mala eleccion de metodo;
- sobreinterpretacion de datos.

Salida:

```markdown
## Riesgos del uso de IA
## Resguardos metodologicos
```

### 17. Iteracion Y Replanteamiento

La app debe reconocer que el diseno de investigacion no es lineal.

Debe permitir:

- volver a conversaciones anteriores;
- reabrir pregunta;
- cambiar objetivos;
- ajustar metodo;
- cambiar datos disponibles;
- comparar versiones;
- recalcular coherencia;
- explicar consecuencias del cambio.

Salida:

```markdown
## Historial metodologico

| Fecha | Decision | Motivo | Impacto en diseno |
|---|---|---|---|
```

### 18. Control De Impacto De Cambios

Cada cambio debe compararse contra el plan original.

La app debe mostrar:

- que parte del diseno cambia;
- que objetivos se ven afectados;
- que metodo queda desalineado;
- que datos dejan de servir;
- que nuevos datos se requieren;
- que afirmaciones ya no se pueden sostener;
- que oportunidades abre el cambio;
- si conviene aceptar, ajustar o rechazar la nueva ruta.

Salida:

```markdown
## Control de cambios metodologicos

| Cambio propuesto | Impacto en pregunta | Impacto en objetivos | Impacto en metodo | Impacto en datos | Decision |
|---|---|---|---|---|---|
```

Opciones:

- Aceptar cambio.
- Ajustar cambio.
- Mantener plan original.

### 19. Auditoria Final

Checklist:

- Que afirmaciones requieren fuente?
- Que decisiones tomo el investigador?
- Que aporto la IA?
- Que fue validado manualmente?
- Que limites deben declararse?
- Que sesgos quedan abiertos?
- El metodo responde a la pregunta?
- Los datos permiten sostener las afirmaciones?
- Esta clara la responsabilidad autoral?

## 10. Comportamiento Del Agente

El agente debe:

- preguntar antes de concluir;
- detectar afirmaciones vagas;
- exigir justificacion;
- distinguir tema, problema, pregunta, objetivos, tesis, metodo y datos;
- revisar atingencia entre disciplina y metodo;
- revisar coherencia entre pregunta y objetivos;
- revisar coherencia entre objetivos, datos y analisis;
- no inventar fuentes;
- advertir limites;
- registrar decisiones;
- sugerir proximos pasos;
- mostrar impacto de cambios.

El agente no debe:

- escribir conclusiones sin evidencia;
- simular certeza;
- inventar referencias;
- aceptar afirmaciones demasiado amplias;
- reemplazar criterio experto;
- presentar correlaciones como causalidad;
- ignorar restricciones eticas o legales de datos;
- permitir cambios de diseno sin mostrar consecuencias.

## 11. Reglas Criticas

### Regla 1: Justificacion

> Todo lo que requiera justificacion debe ser justificado.

### Regla 2: Pregunta

> La pregunta manda. Los objetivos obedecen. El metodo responde. Los datos sostienen.

### Regla 3: Disciplina

Si el usuario no esta bien situado disciplinariamente, la app debe ayudar a aclarar desde donde habla.

### Regla 4: Metodo

Si el metodo no responde la pregunta, la app debe detenerse.

### Regla 5: Datos

Si los datos no permiten sostener una afirmacion, la app debe advertirlo.

### Regla 6: Cambios

> Cambiar de ruta esta permitido; hacerlo sin saber que rompe, no.

### Regla 7: IA

Si la IA esta siendo usada para reemplazar pensamiento experto, la app debe reconducir el proceso.

## 12. Ejemplos De Alertas

**Afirmacion vaga**

> La IA mejora la investigacion.

Respuesta:

> Esa afirmacion es demasiado general. Mejora velocidad, calidad, acceso, escritura, revision, analisis o productividad? Que evidencia lo sostendria?

**Objetivo desalineado**

> La pregunta busca comprender percepciones, pero el objetivo general habla de evaluar impacto. Deben alinearse.

**Objetivo especifico como tarea**

> "Revisar literatura" no es un objetivo especifico de investigacion; es una actividad. Un objetivo seria "Identificar los principales enfoques teoricos sobre...".

**Metodo no atingente**

> Una encuesta puede estudiar percepciones o adopcion organizacional, pero no demuestra por si sola una afirmacion juridica.

**Datos insuficientes**

> Las entrevistas pueden aportar experiencias e interpretaciones, pero no permiten medir impacto causal.

**Cambio de diseno**

> Cambiar de impacto a percepciones es viable, pero obliga a reformular pregunta, objetivos, metodo y tipo de conclusion.

## 13. Entregable MVP

La app debe generar:

```markdown
# Ficha de investigacion

## Tipo de producto
## Area tematica
## Disciplina principal
## Disciplinas secundarias
## Comunidad academica objetivo

## Enfoques considerados
## Enfoque elegido
## Justificacion disciplinar

## Tema
## Problema
## Pregunta central
## Objetivo general
## Objetivos especificos
## Tesis o hipotesis

## Metodos atingentes
## Metodo elegido
## Justificacion del metodo

## Datos disponibles
## Datos necesarios
## Fuente de datos
## Unidad de analisis
## Nivel de agregacion
## Calidad de datos
## Restricciones eticas o legales

## Matriz objetivo-datos-analisis
## Plan de procesamiento de datos
## Tecnicas de analisis
## Resultados esperados
## Limites de interpretacion

## Auditoria de coherencia
## Control de cambios metodologicos

## Uso de IA por etapa
## Riesgos
## Resguardos
## Decisiones metodologicas
## Proximo paso
```

## 14. Metricas De Exito

MVP exitoso si:

- un usuario pasa de idea vaga a ficha estructurada en menos de 30 minutos;
- la ficha distingue area, disciplina, pregunta, objetivos, metodo y datos;
- la app identifica inconsistencias entre pregunta y objetivos;
- la app identifica inconsistencias entre metodo y disciplina;
- la app conecta objetivos con datos y tecnicas de analisis;
- la app muestra impacto de cambios metodologicos;
- la app identifica al menos 3 riesgos del uso de IA;
- la app exige justificacion en afirmaciones vagas;
- el usuario entiende que falta validar;
- el resultado puede usarse como insumo para paper, tesis, informe, post o taller.

## 15. Version 2

Posibles extensiones:

- carga de documentos;
- lectura de bases de datos;
- sugerencia de tecnicas de analisis;
- generacion de protocolo institucional de IA;
- exportacion DOCX/PDF;
- integracion con Obsidian;
- integracion con Zotero;
- integracion con repositorios de datos;
- historial robusto de decisiones;
- auditoria de trazabilidad;
- colaboracion por equipos;
- agentes por etapa metodologica;
- panel docente para guiar tesis.

## 16. Riesgos Del Producto

- Que se perciba como otro chatbot.
- Que el usuario espere que escriba todo.
- Que el agente sea demasiado complaciente.
- Que genere falsa seguridad metodologica.
- Que el flujo sea muy largo.
- Que investigadores expertos lo sientan basico.
- Que usuarios novatos no entiendan categorias metodologicas.
- Que el producto sobrecargue de preguntas antes de ayudar.
- Que parezca una plantilla rigida y no un interlocutor.

## 17. Principio De Diseno

Investigadopedia debe sentirse como:

- un editor metodologico;
- un tutor exigente;
- un auditor de razonamiento;
- un companero de investigacion;
- un sistema de trazabilidad.

No debe sentirse como:

- una plantilla rigida;
- un generador de papers;
- un chatbot generico;
- un curso disfrazado de app.

## 18. Frases De Producto

> Investigadopedia no escribe por ti: te ayuda a formular mejor, justificar mejor, analizar mejor y dejar rastro de como investigaste con IA.

> La pregunta manda. Los objetivos obedecen. El metodo responde. Los datos sostienen. Las conclusiones no pueden decir mas que la evidencia permite.

> Cambiar de ruta esta permitido; hacerlo sin saber que rompe, no.
