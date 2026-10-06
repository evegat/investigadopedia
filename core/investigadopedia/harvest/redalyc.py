"""
Harvester de Redalyc para Investigadopedia.
Aprovecha que OpenAlex indexa Redalyc bajo dos fuentes de repositorio (~371k obras):
  - S4377196100: Redalyc (UAEM) (~288,000 obras)
  - S4306402163: Redalyc (UAEM) (~83,000 obras)
Permite búsqueda booleana real sobre Redalyc sin depender del endpoint roto OAI-PMH.
(Ver referencias e inspiraciones en CREDITS.md).
"""

import json
from pathlib import Path
from typing import Generator, Dict, Any, Optional
from .openalex import iterate_openalex_works


REDALYC_SOURCE_FILTER = "locations.source.id:S4377196100|S4306402163"


def search_redalyc(
    query: str,
    max_records: int = 200,
    out_path: Optional[str] = None,
) -> Generator[Dict[str, Any], None, None]:
    """Ejecuta una búsqueda por palabras clave sobre el universo de Redalyc."""
    works = iterate_openalex_works(
        filter_expr=REDALYC_SOURCE_FILTER,
        search_query=query,
        max_records=max_records,
        source_engine="redalyc_via_openalex",
    )

    if not out_path:
        for w in works:
            yield w
        return

    # Si se pide escribir a disco, uso de escritura atómica
    out_file = Path(out_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file = out_file.with_suffix(f"{out_file.suffix}.tmp")

    count = 0
    with open(temp_file, "w", encoding="utf-8") as f:
        for w in works:
            f.write(json.dumps(w, ensure_ascii=False) + "\n")
            count += 1
            yield w

    temp_file.replace(out_file)
