# ODD Task: Módulo Match (JANE Latam para Ciencias Sociales)

## 1. Contexto y Problema
En América Latina y el Caribe, los investigadores en Ciencias Sociales y Humanidades enfrentan una brecha crítica: las herramientas de recomendación de revistas (JANE) están sesgadas a biomedicina (PubMed), mientras que las alternativas comerciales (Elsevier JournalFinder, Springer) priorizan publicaciones anglosajonas con altas tarifas de APC.
Los índices regionales soberanos (SciELO Social Sciences, Redalyc, Latindex Catálogo 2.0 y Dialnet) operan bajo el modelo Acceso Abierto Diamante (sin costo para autor ni lector), pero carecen de motores semánticos de coincidencia por título/resumen.

## 2. Objetivo
Construir el submódulo `investigadopedia.match` y el comando CLI `investigadopedia match` para:
1. Recomendar revistas indexadas en Iberoamérica (SciELO / Redalyc / Latindex) a partir de un título y/o abstract de Ciencias Sociales.
2. Identificar autores y potenciales revisores por pares en la región.
3. Clasificar por modelo de acceso (Diamante / APC-free) y nivel de indexación regional/global.
4. Mantener cero dependencias externas (Python 3.8+ estándar) con fallback heurístico determinista sin conexión obligatoria.

## 3. Criterios de Aceptación (DoD)
- [x] Función `scramble_text(text: str) -> str` para protección de privacidad en clientes locales.
- [x] Catálogo de revistas de Ciencias Sociales de Iberoamérica con ISSNs, nombres, países, indexaciones y modelo de acceso.
- [x] Algoritmo de similitud léxica/semántica (Jaccard / TF ponderado sobre n-gramas y conceptos) entre el abstract ingresado y los perfiles de revistas.
- [x] Agrupación y ponderación de autores/revisores frecuentes según trabajos coincidentes.
- [x] Comando CLI `investigadopedia match --text "..." [--out reporte.md]`.
- [x] Suite de pruebas unitarias TDD verdes en `tests/test_match.py`.
- [x] Integración verificada en `test_core.py` (12 tests pasando en suite unificada).
