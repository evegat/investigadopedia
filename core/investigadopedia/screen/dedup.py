"""
Módulo de deduplicación y consolidación de corpus para Investigadopedia.
(Ver referencias e inspiraciones en CREDITS.md):
- Prioridad de unificación por DOI limpio.
- Fallback a título normalizado compatible con alfabetos no-latinos (Cyrillic, CJK, etc.).
- Preservación y unión de proveniencia (source engines).
- Limpieza de separadores de línea Unicode no estándar (U+2028, U+2029, U+0085).
"""

import json
import re
import unicodedata
from pathlib import Path
from typing import Dict, List, Any, Optional


def clean_line_breaks(text: Optional[str]) -> Optional[str]:
    """Elimina separadores de línea no estándar que corrompen formatos JSONL."""
    if not text:
        return text
    return text.replace("\u2028", " ").replace("\u2029", " ").replace("\u0085", " ")


def normalize_doi(doi: Optional[str]) -> Optional[str]:
    """Normaliza un DOI eliminando prefijos http/https/doi.org y pasando a minúsculas."""
    if not doi:
        return None
    cleaned = doi.strip().lower()
    cleaned = re.sub(r"^https?://(dx\.)?doi\.org/", "", cleaned)
    cleaned = re.sub(r"^doi:\s*", "", cleaned)
    return cleaned if cleaned else None


def normalize_title(title: Optional[str]) -> str:
    """Normaliza un título para deduplicación:
    - Minúsculas y normalización Unicode NFKC.
    - Remoción de acentos latinos específicos (á, é, í, ó, ú, etc.) sin alterar alfabetos no-latinos (Cyrillic, CJK, etc.).
    - Remoción de puntuación y espacios redundantes.
    """
    if not title:
        return ""
    lowered = title.lower()
    accents_map = {
        "á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ü": "u",
        "à": "a", "è": "e", "ì": "i", "ò": "o", "ù": "u",
        "â": "a", "ê": "e", "î": "i", "ô": "o", "û": "u",
        "ã": "a", "õ": "o",
    }
    stripped = "".join(accents_map.get(ch, ch) for ch in lowered)
    stripped = unicodedata.normalize("NFKC", stripped)
    # Eliminar signos de puntuación comunes manteniendo letras y números de cualquier idioma
    normalized = re.sub(r"[^\w\s]", "", stripped)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def merge_jsonl_files(input_paths: List[str], output_path: str) -> int:
    """Combina múltiples archivos JSONL deduplicando por DOI o título normalizado."""
    records_by_key: Dict[str, Dict[str, Any]] = {}

    for path_str in input_paths:
        path = Path(path_str)
        if not path.exists():
            continue

        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = clean_line_breaks(line.strip())
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except Exception:
                    continue

                doi_key = normalize_doi(record.get("doi"))
                title_key = normalize_title(record.get("title"))

                dedup_key = f"doi:{doi_key}" if doi_key else f"title:{title_key}"
                if not dedup_key or dedup_key == "title:":
                    continue

                if dedup_key in records_by_key:
                    # Fusión de proveniencia
                    existing = records_by_key[dedup_key]
                    existing_sources = set(existing.get("source_engines", [existing.get("source_engine")]))
                    new_source = record.get("source_engine")
                    if new_source:
                        existing_sources.add(new_source)
                    existing["source_engines"] = sorted(list(filter(None, existing_sources)))
                    # Completar abstract si el existente no lo tenía
                    if not existing.get("abstract") and record.get("abstract"):
                        existing["abstract"] = clean_line_breaks(record["abstract"])
                else:
                    source = record.get("source_engine")
                    record["source_engines"] = [source] if source else []
                    record["abstract"] = clean_line_breaks(record.get("abstract"))
                    records_by_key[dedup_key] = record

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file = out_file.with_suffix(f"{out_file.suffix}.tmp")

    with open(temp_file, "w", encoding="utf-8") as f:
        for rec in records_by_key.values():
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    temp_file.replace(out_file)
    return len(records_by_key)
