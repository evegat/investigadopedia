---
tipo: pendiente
proyecto: EDI001
estado: en_progreso
fecha: 2026-10-09
prioridad: alta
custodia:
  owner: antigravity
  host: EVT
  session: 188a2bb2-dbbe-4a4f-b5f7-a026c263dba9
---

# Pendiente — Habilitadores para Lanzamiento GO de Investigadopedia

Plan de ejecución inmediata para alcanzar el veredicto **GO oficial**:

1. [ ] **Privacidad y OpenAlex 100% Opt-in**: Desmarcar por defecto `#chk-live-authors` en `web/index.html` y clarificar banner de privacidad.
2. [ ] **Corrección de ISSNs y Enlaces a Revistas**: Corregir ISSNs de EURE y Ciencia Política, y completar URLs de las 21 revistas en `web/data/journals.json` y `core/investigadopedia/match/catalog.py`.
3. [ ] **Honestidad en Roadmap**: Quitar `baseVotes` artificiales y rotular votos locales.
4. [ ] **Licencia**: Crear archivo `LICENSE` (MIT) en la raíz del repositorio.
5. [ ] **Gates y Deploy**: Correr suite de tests (22 tests), gates quality/security del arnés y desplegar en Coolify.
