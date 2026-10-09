---
tipo: recurso
proyecto: EDI001
subtipo: roadmap
estado: activo
actualizado: 2026-10-06
url_produccion: https://investigadopedia.evegat.cl
repositorio: https://github.com/evegat/investigadopedia
---

# Investigadopedia — Catastro de Funcionalidades, Mejoras y Hoja de Ruta

Inventario vivo de requerimientos, funcionalidades y mejoras para el ecosistema de **Investigadopedia** (`EDI001`), organizado por horizonte de desarrollo y área de impacto.

---

## 1. Módulo "Dónde Publicar" (Recomendador de Revistas y Pares)

### En Producción (v1.0.0)
- [x] Motor de cálculo léxico 100% en el navegador (sin envío de manuscritos a servidores propios).
- [x] Filtro estricto de Acceso Abierto Diamante ($0 cobro por APC a autores).
- [x] Botón de anonimización léxica (*Desordenar palabras*) para proteger primicias intelectuales.
- [x] Extracción en vivo de autores afines vía OpenAlex mediante consultas con resguardo de privacidad (*Zero-Knowledge*).
- [x] Catálogo inicial curado de 21 revistas indexadas en SciELO, Redalyc y Latindex 2.0.

### Mejoras Inmediatas (Horizonte Corto Plazo / Quick Wins)
- [ ] **Arrastre de Documentos (Drag & Drop PDF/DOCX)**:
  - Extracción automática local del título y resumen en el navegador sin tener que copiar/pegar manualmente.
- [ ] **Ampliación de Cobertura Disciplinar (50+ revistas)**:
  - Incorporar Antropología, Historia, Psicología Social, Geografía Humana, Filosofía y Lingüística.
  - Añadir revistas diamante de Brasil en portugués (ej. *Dados*, *Tempo Social*, *Mana*).
- [ ] **Filtro por Indexación Múltiple**:
  - Checkboxes para filtrar solo revistas que estén simultáneamente en SciELO + Scopus, o solo Latindex Catálogo 2.0.
- [ ] **Enlace Directo a Envíos OJS**:
  - Botón de 1 clic para ir a la página exacta de sumisiones (`/about/submissions`) de la revista seleccionada.

### Funcionalidades Avanzadas (Horizonte Mediano Plazo)
- [ ] **Estimador de Tiempos de Arbitraje y Publicación**:
  - Cálculo de meses promedio entre recepción, dictamen y publicación basado en metadatos reales de artículos recientes.
- [ ] **Exportador de Ficha de Postulación**:
  - Descarga en Markdown/PDF con la terna de revisores sugeridos sin conflicto de interés, checklist de pautas y plantilla formal.
- [ ] **Verificador de Ausencia de Conflicto de Interés**:
  - Filtro para descartar evaluadores con la misma afiliación institucional o coautorías con el usuario.

---

## 2. Módulo "Catálogo de Habilidades y Recursos" (Estilo aitmpl.com)

### En Producción (v1.0.0)
- [x] Buscador interactivo en tiempo real con atajo global `Ctrl + K` / `⌘K`.
- [x] Filtros por categorías con contadores dinámicos (*Habilidades y Métodos*, *Prompts y Tutores*, *Bases y Cosecha*, *Observatorios y Repos*).
- [x] Fichas modulares con previsualización, etiquetas y botón de copia rápida al portapapeles.
- [x] Integración de 9 componentes curados (Vigilancia Epistemológica, Cribador PRISMA, Cosecha SciELO/Redalyc, Tutor Socrático, Cover Letter y observatorios cívicos).

### Mejoras Inmediatas
- [ ] **Descarga directa de plantillas (`.md` / `.txt`)**:
  - Botón para descargar el prompt o matriz en un archivo limpio sin necesidad de copiar y pegar.
- [ ] **Filtro multifaceta por etiquetas**:
  - Poder filtrar simultáneamente por etiqueta (ej. `#SciELO` + `#Metodología`).
- [ ] **Visualizador de versión ejecutable**:
  - Ejemplo concreto de *Input* y *Output* para cada prompt o habilidad pedagógica.

### Componentes y Habilidades a Incorporar
- [ ] **Prompt de Auditoría de Citas Fantasma**:
  - Detector de alucinaciones en referencias bibliográficas para contrastar con DOIs reales.
- [ ] **Matriz de Operacionalización de Variables Cualitativas/Cuantitativas**:
  - Asistente para conectar dimensiones teóricas con indicadores empíricos observables.
- [ ] **Protocolo de Transcripción y Codificación Asistida**:
  - Pauta metodológica para análisis temático y de contenido cualitativo asistido por IA.
- [ ] **Conector SciELO Harvester CLI**:
  - Script descargable en Python para automatizar descargas masivas de metadatos locales.

---

## 3. Módulo "Tutor Mayéutico e Interlocutor Riguroso" (Core Metodológico PRD)

### Estado Actual
- Ficha conceptual y diseño de System Prompt desarrollados en `System Prompt - Tutor Mayeutico.md` y `Ficha Articulo Mayeutica.md`.

### Funcionalidades en Hoja de Ruta
- [ ] **Interlocutor Mayéutico Interactivo en Vivo**:
  - Chat socrático integrado en la web (usando modelo local en navegador WebLLM o API BYOK - *Bring Your Own Key*).
  - El tutor no escribe el texto: interroga agresivamente las debilidades del diseño.
- [ ] **Generador de Ficha de Coherencia Metodológica**:
  - Evaluación automática de la alineación entre:
    1. Pregunta de investigación.
    2. Objetivos específicos.
    3. Marco teórico.
    4. Universo y muestra.
    5. Técnica de recolección y análisis.
- [ ] **Detector de Brechas y Saltos Argumentales**:
  - Módulo que marca párrafos donde la conclusión sobrepasa el alcance de los datos.

---

## 4. Módulo "Roadmap Participativo y Comunidad"

### En Producción (v1.0.0)
- [x] Tarjetas dinámicas con conteo de votos persistentes en almacenamiento local.
- [x] Formulario para proponer nuevas revistas y funciones comunitarias.

### Mejoras Inmediatas
- [ ] **Sincronización de Votos en Servidor/Base Liviana**:
  - Conectar los votos a un endpoint liviano (ej. PocketBase o tabla segura) para unificar la votación entre todos los visitantes.
- [ ] **Filtro de Estado de Desarrollo**:
  - Pestañas o etiquetas en las tarjetas del roadmap: *Propuesta*, *En Diseño*, *En Desarrollo*, *Publicado*.
- [ ] **Botón para sugerir revistas latinoamericanas faltantes**:
  - Formulario específico de postulación de revista (Nombre, ISSN, País, Enlace OJS).

---

## 5. Integridad Ética, Privacidad y Soberanía

### En Producción (v1.0.0)
- [x] Pacto explícito de protección de manuscritos e ideas.
- [x] Arquitectura de procesamiento en el cliente sin backend de captura de textos.
- [x] Consulta desacoplada a APIs públicas para evitar filtración de manuscritos inéditos.

### Mejoras a Incorporar
- [ ] **Alerta de Revistas Predadoras o Mercenarias**:
  - Detección de revistas con prácticas dudosas o desindexadas que cobran sumas abusivas.
- [ ] **Verificación de Cumplimiento de Declaraciones de IA**:
  - Guía adaptada a directrices ICMJE, COPE y normativas universitarias locales sobre declaración transparente del uso de IA en la autoría.
- [ ] **Soporte Multilingüe Completo (Español / Portugués / Inglés)**:
  - Traducción nativa de la interfaz para acoger a investigadores de Brasil y el resto de la región.

---

## 6. Infraestructura y Calidad de Ingeniería (Arnés MyWorld v1)

- [x] 22/22 pruebas unitarias automatizadas (`test_core.py`, `test_match.py`, `test_web_resilience.py`).
- [x] Gates de calidad y seguridad integrados (`quality: pass`, `security: pass` con Gitleaks y Trivy).
- [x] Despliegue continuo probado en VPS Coolify + Cloudflare SSL en `investigadopedia.evegat.cl`.
- [ ] Integración de pipeline GitHub Actions para ejecución remota de gates en cada push.
