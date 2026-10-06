"""
Módulo de partición de literatura (Académica vs Gris vs Descartada) para Investigadopedia.
(Ver referencias e inspiraciones en CREDITS.md):
Hace física la costura entre literatura indexada revisada por pares y literatura gris/preprints.
"""

import json
from pathlib import Path
from typing import Dict, Any


def partition_corpus(input_path: str, output_dir: str) -> Dict[str, int]:
    """Particiona un archivo JSONL en 3 cubetas y emite un informe de proveniencia."""
    in_file = Path(input_path)
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    academic_records = []
    grey_records = []
    dropped_records = []

    with open(in_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except Exception:
                continue

            title = (rec.get("title") or "").strip()
            if not title or len(title) < 5:
                dropped_records.append(rec)
                continue

            venue = (rec.get("venue") or "").lower()
            issn = rec.get("issn_l")
            doi = rec.get("doi")
            sources = rec.get("source_engines", [])

            # Criterio de exención SciELO/Redalyc:
            # Artículos provenientes de SciELO o Redalyc son considerados automáticamente académicos.
            is_regional_verified = any("scielo" in s or "redalyc" in s for s in sources)

            # Si es preprint o repositorio
            is_preprint = any(kw in venue for kw in ["arxiv", "biorxiv", "medrxiv", "ssrn", "zenodo", "repository", "repositorio"])

            if is_regional_verified or (issn and not is_preprint) or (doi and not is_preprint and venue and "sin revista" not in venue):
                academic_records.append(rec)
            elif is_preprint or not issn:
                grey_records.append(rec)
            else:
                dropped_records.append(rec)

    # Escrituras atómicas
    def write_jsonl(path: Path, data):
        temp = path.with_suffix(f"{path.suffix}.tmp")
        with open(temp, "w", encoding="utf-8") as f:
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        temp.replace(path)

    write_jsonl(out_dir / "corpus_academic.jsonl", academic_records)
    write_jsonl(out_dir / "corpus_grey.jsonl", grey_records)
    write_jsonl(out_dir / "corpus_dropped.jsonl", dropped_records)

    report = {
        "total_records": len(academic_records) + len(grey_records) + len(dropped_records),
        "academic_peer_reviewed": len(academic_records),
        "grey_literature": len(grey_records),
        "dropped_invalid": len(dropped_records),
        "academic_percentage": round((len(academic_records) / max(1, (len(academic_records) + len(grey_records) + len(dropped_records)))) * 100, 2),
    }

    with open(out_dir / "provenance_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return report
