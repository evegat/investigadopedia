"""
Harvester de SciELO para Investigadopedia.
Constriñe la búsqueda en OpenAlex al universo de ISSNs de las revistas indexadas en SciELO
(~2.274 revistas a través de 24 colecciones regionales de América Latina, Caribe, Iberia y Sudáfrica).
(Ver referencias e inspiraciones en CREDITS.md).
"""

import json
from pathlib import Path
from typing import Generator, Dict, Any, Optional, List
from .openalex import iterate_openalex_works, fetch_openalex_page


# Colección de prueba / representativa de ISSNs destacados de SciELO para testing rápido
SAMPLE_SCIELO_ISSNS = [
    "0034-8910",  # Revista de Saúde Pública (Brasil)
    "0717-7348",  # Revista chilena de enfermedades respiratorias
    "0718-0764",  # Información tecnológica (Chile)
    "0120-0011",  # Revista de la Facultad de Medicina (Colombia)
    "0185-1667",  # Investigación económica (México)
    "0718-2724",  # Journal of technology management & innovation (Chile)
    "0718-0934",  # Revista signos (Chile)
    "0034-9887",  # Revista médica de Chile
    "0717-6996",  # EURE (Santiago)
    "0718-2236",  # Revista de ciencia política (Santiago)
]


def build_issn_chunk_filter(issns: List[str]) -> str:
    """Construye una cláusula OR de ISSNs para OpenAlex."""
    cleaned = [issn.strip().replace("-", "") for issn in issns if issn.strip()]
    return "primary_location.source.issn:" + "|".join(cleaned)


def search_scielo_by_issns(
    query: str,
    issns: Optional[List[str]] = None,
    max_records: int = 200,
    out_path: Optional[str] = None,
) -> Generator[Dict[str, Any], None, None]:
    """Ejecuta una búsqueda de literatura en OpenAlex restringida al universo de revistas SciELO."""
    target_issns = issns or SAMPLE_SCIELO_ISSNS
    filter_expr = build_issn_chunk_filter(target_issns)

    works = iterate_openalex_works(
        filter_expr=filter_expr,
        search_query=query,
        max_records=max_records,
        source_engine="scielo_via_openalex_issns",
    )

    if not out_path:
        for w in works:
            yield w
        return

    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file = out_file.with_suffix(f"{out_file.suffix}.tmp")

    with open(temp_file, "w", encoding="utf-8") as f:
        for w in works:
            f.write(json.dumps(w, ensure_ascii=False) + "\n")
            yield w

    temp_file.replace(out_file)
