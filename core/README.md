# Investigadopedia Core v1.0.0

Toolkit autónomo de investigación científica sin dependencias externas pesadas (Python 3.8+ estándar).

## Características Principales

1. **Cosecha Regional y Global (Harvest):**
   - Búsqueda booleana real sobre **SciELO** y **Redalyc** a través del universo OpenAlex (técnicas documentadas en `CREDITS.md`).
   - Reconstrucción fiel de abstracts invertidos.
   - Fail Loud: nunca retorna 0 silencioso ante fallos de conexión o cuota.
2. **Deduplicación & Partición Física:**
   - Unificación por DOI normalizado y título no-Latin safe (preserva caracteres Cyrillic, CJK, acentos).
   - Costura física entre literatura académica arbitrada (`corpus_academic.jsonl`) y literatura gris (`corpus_grey.jsonl`).
3. **Cribado Acelerado (Screening):**
   - Conector con **TypeSafe Jev (System 1 RLCD)** para clasificar 1.000+ papers en minutos a costo mínimo ($0.042/1M tokens).
   - Fallback heurístico determinista sin internet ni API keys.
4. **Vigilancia Epistemológica:**
   - Auditoría estricta de la tripartición: Hecho Observado vs. Inferencia Fundada vs. Supuesto/Brecha.
5. **Reportes PRISMA 2020:**
   - Generación automática de diagramas Mermaid y tablas de conteo de flujo.

## Instalación

```bash
# Instalación local editable
pip install -e .
```

## Uso Rápido CLI

```bash
# 1. Cosechar literatura
investigadopedia harvest --engine redalyc --query "politicas publicas" --max 50 --out redalyc.jsonl
investigadopedia harvest --engine scielo --query "politicas publicas" --max 50 --out scielo.jsonl

# 2. Fusionar y deduplicar
investigadopedia merge --inputs redalyc.jsonl scielo.jsonl --out merged.jsonl

# 3. Particionar por calidad y arbitraje
investigadopedia partition --input merged.jsonl --out-dir ./partition/

# 4. Cribar por relevancia PRISMA
investigadopedia screen --input ./partition/corpus_academic.jsonl --criteria "impacto en salud o educacion" --out screened.jsonl

# 5. Auditar manuscrito
investigadopedia audit-text --file borrador_paper.md
```
