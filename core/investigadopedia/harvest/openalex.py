"""
Motor de consulta OpenAlex para Investigadopedia.
Stdlib puro (sin dependencias).
Reconstrucción de abstracts invertidos y políticas de fallo ruidoso (Fail Loud).
"""

import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Generator, List, Optional


class OpenAlexQueryFailed(RuntimeError):
    """Excepción alzada cuando OpenAlex falla o se agota la cuota.
    Nunca se debe retornar 0 resultados silenciosos ante un error de red o API.
    """
    pass


def reconstruct_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> Optional[str]:
    """Reconstruye un abstract en texto continuo a partir del inverted index de OpenAlex."""
    if not inverted_index:
        return None
    try:
        word_positions: List[tuple] = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((pos, word))
        word_positions.sort(key=lambda x: x[0])
        return " ".join(word for _, word in word_positions)
    except Exception:
        return None


def fetch_openalex_page(
    filter_expr: str,
    search_query: Optional[str] = None,
    cursor: str = "*",
    per_page: int = 100,
    mailto: Optional[str] = None,
    api_key: Optional[str] = None,
    max_retries: int = 3,
) -> Dict[str, Any]:
    """Consulta una página individual en la API de OpenAlex vía cursor-based pagination."""
    api_key = api_key or os.getenv("OPENALEX_API_KEY")
    mailto = mailto or os.getenv("OPENALEX_MAILTO", "eduardo@myworld.local")

    params = {
        "filter": filter_expr,
        "per-page": str(per_page),
        "cursor": cursor,
    }
    if search_query:
        params["search"] = search_query
    if mailto:
        params["mailto"] = mailto
    if api_key:
        params["api_key"] = api_key

    query_str = urllib.parse.urlencode(params)
    url = f"https://api.openalex.org/works?{query_str}"

    headers = {
        "User-Agent": f"Investigadopedia-Harvest/1.0 (mailto:{mailto})",
        "Accept": "application/json",
    }

    last_error = None
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=30) as resp:
                if resp.status == 200:
                    return json.loads(resp.read().decode("utf-8"))
                else:
                    raise OpenAlexQueryFailed(f"OpenAlex HTTP {resp.status}: {resp.reason}")
        except urllib.error.HTTPError as e:
            last_error = e
            if e.code == 429:
                # Rate limit de OpenAlex: pausa más prolongada
                time.sleep(3.0 * (attempt + 1))
            else:
                time.sleep(1.0 * (attempt + 1))
        except Exception as e:
            last_error = e
            time.sleep(1.5 * (attempt + 1))

    raise OpenAlexQueryFailed(f"Falló la consulta OpenAlex tras {max_retries} intentos en {url}: {last_error}")


def flatten_work(work: Dict[str, Any], source_engine: str) -> Dict[str, Any]:
    """Normaliza un objeto Work de OpenAlex al esquema estándar de Investigadopedia."""
    doi = work.get("doi")
    title = work.get("title") or ""
    publication_year = work.get("publication_year")
    
    # Extraer autores
    authors = []
    for authorship in work.get("authorships", []):
        author_obj = authorship.get("author", {})
        if author_obj.get("display_name"):
            authors.append(author_obj["display_name"])
            
    # Extraer venue / revista
    primary_loc = work.get("primary_location") or {}
    source = primary_loc.get("source") or {}
    venue_name = source.get("display_name") or "Sin revista registrada"
    issn_l = source.get("issn_l")
    
    # Open Access
    oa_info = work.get("open_access") or {}
    is_oa = oa_info.get("is_oa", False)
    oa_url = oa_info.get("oa_url")
    
    # Abstract
    abstract = reconstruct_abstract(work.get("abstract_inverted_index"))

    return {
        "id": work.get("id"),
        "doi": doi,
        "title": title.strip(),
        "publication_year": publication_year,
        "publication_date": work.get("publication_date"),
        "authors": authors,
        "venue": venue_name,
        "issn_l": issn_l,
        "abstract": abstract,
        "language": work.get("language"),
        "is_oa": is_oa,
        "oa_url": oa_url,
        "cited_by_count": work.get("cited_by_count", 0),
        "source_engine": source_engine,
        "concepts": [c.get("display_name") for c in work.get("concepts", [])[:5]],
    }


def iterate_openalex_works(
    filter_expr: str,
    search_query: Optional[str] = None,
    max_records: int = 500,
    source_engine: str = "openalex",
) -> Generator[Dict[str, Any], None, None]:
    """Generador que pagina sobre OpenAlex y entrega registros normalizados."""
    cursor = "*"
    yielded = 0

    while cursor and yielded < max_records:
        data = fetch_openalex_page(filter_expr=filter_expr, search_query=search_query, cursor=cursor)
        results = data.get("results", [])
        if not results:
            break

        for item in results:
            yield flatten_work(item, source_engine=source_engine)
            yielded += 1
            if yielded >= max_records:
                break

        cursor = data.get("meta", {}).get("next_cursor")
        if not cursor:
            break
        time.sleep(0.1)  # Cortesía de red
