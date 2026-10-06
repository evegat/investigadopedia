# ODD Task: Privacidad Explícita y Blindaje de Resiliencia para Investigadopedia Web

## 1. Contexto y Problema
Al publicar `investigadopedia.evegat.cl` para terceros, existen dos riesgos críticos:
1. **Desconfianza del investigador:** Los autores temen pegar borradores inéditos por miedo al plagio, entrenamiento no consentido de LLMs o espionaje editorial. Es imperativo transparentar técnica y jurídicamente cómo se resguardan sus ideas.
2. **Caídas y Denegación de Servicio (DoS):** Si la página se viraliza o terceros abusan de llamadas a APIs externas (OpenAlex) o intentan inyecciones maliciosas (XSS), el servicio no debe caerse ni bloquear a los usuarios legítimos.

## 2. Solución Arquitectónica
- **Cuidado de Ideas (Zero-Knowledge):**
  - Declaración explícita y visible de Soberanía y Privacidad de Datos en la UI.
  - El abstract completo NUNCA sale del navegador. Solo los términos temáticos genéricos tokenizados se usan para la API de autores.
  - Botón Scramble con explicación didáctica y verificable.
- **Blindaje Anticaídas (Resiliencia Extrema):**
  - Frontend servido en el borde (Edge CDN Cloudflare Pages) con WAF y protección anti-DDoS inherente.
  - Sanitización estricta de texto (prevención XSS contra inyección en el DOM).
  - Cache en `sessionStorage` para no duplicar peticiones de OpenAlex.
  - Throttling / Debounce en botones de búsqueda.
  - Fail-soft absoluto: si OpenAlex falla o se satura (HTTP 429), la app continúa entregando el 100% de las revistas recomendadas desde el catálogo local sin romperse.

## 3. Criterios de Aceptación (DoD)
- [x] Módulo/Modal explicativo visible: *"Pacto de Protección de Ideas e Integridad Intelectual"*.
- [x] Sanitización rigurosa de input contra XSS en `app.js` (`escapeHtml`).
- [x] Resguardo de consultas externas: la llamada a OpenAlex solo transmite 1 o 2 términos lematizados, jamás oraciones ni abstracts.
- [x] Cache local en navegador (`sessionStorage`) para mitigar saturación de red.
- [x] Fallback silencioso y elegante ante desconexión o bloqueo de API externa (Zero-Crash).
- [x] Pruebas unitarias de sanitización y resiliencia en `tests/test_web_resilience.py` (3 tests pasando).
- [x] Registro en Engram y actualización de bitácora/Home.
