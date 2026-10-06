"""
Motor de estimación y coincidencia de revistas y autores (JANE Latam Ciencias Sociales).
Permite calcular afinidad semántica y léxica entre un abstract/título y el corpus de revistas
de Ciencias Sociales de América Latina y el Caribe.
"""

import re
import unicodedata
from typing import List, Dict, Any, Optional
from .catalog import get_latam_social_science_journals, LatamJournal
from ..harvest.openalex import fetch_openalex_page


STOPWORDS_IBEROAMERICA = {
    # Español
    "el", "la", "los", "las", "un", "una", "unos", "unas", "de", "del", "a", "al", "en",
    "y", "o", "u", "e", "con", "por", "para", "sobre", "entre", "sin", "tras", "desde",
    "hasta", "hacia", "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas",
    "aquel", "aquella", "su", "sus", "mi", "mis", "tu", "tus", "nuestro", "nuestra",
    "que", "cual", "quien", "cuyo", "donde", "cuando", "como", "mas", "pero", "sino",
    "porque", "pues", "ya", "se", "lo", "le", "les", "me", "te", "nos", "os", "es", "son",
    "fue", "eran", "ser", "estar", "ha", "han", "hay", "articulo", "analiza", "evalua",
    "presenta", "estudia", "estudio", "investigacion", "trabajo", "resultados", "metodologia",
    "demostramos", "demuestra", "mostramos", "muestra", "concluimos", "concluye", "proponemos", "propone", "plantea", "planteamos",
    # Portugués
    "o", "a", "os", "as", "um", "uma", "uns", "umas", "do", "da", "dos", "das", "no", "na",
    "nos", "nas", "em", "de", "para", "com", "por", "que", "e", "se", "ao", "aos",
    "este", "esta", "estes", "estas", "esse", "essa", "esses", "essas", "seu", "sua",
    "seus", "suas", "artigo", "analisa", "estudo", "pesquisa", "resultados"
}


def normalize_token(text: str) -> str:
    """Normaliza un token eliminando tildes y pasando a minúsculas."""
    if not text:
        return ""
    nfkd = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def extract_content_words(text: str) -> List[str]:
    """Extrae palabras de contenido descartando stopwords y signos ortográficos."""
    raw_tokens = re.split(r"[^\w]+", text.lower())
    words = []
    for t in raw_tokens:
        clean = normalize_token(t)
        if clean and len(clean) > 2 and clean not in STOPWORDS_IBEROAMERICA:
            words.append(clean)
    return words


class JournalEstimator:
    """Estimador de afinidad temática para revistas y autores latinoamericanos."""

    def __init__(self, journals: Optional[List[LatamJournal]] = None):
        self.journals = journals or get_latam_social_science_journals()

    def match_journals(
        self,
        text: str,
        top_n: int = 5,
        diamond_only: bool = True,
        min_score: float = 0.05,
    ) -> List[Dict[str, Any]]:
        """Calcula el índice de coincidencia temática entre un texto y las revistas del catálogo."""
        if not text:
            return []

        text_norm = normalize_token(text)
        query_words = set(extract_content_words(text))
        if not query_words:
            return []

        scored_results: List[Dict[str, Any]] = []

        for journal in self.journals:
            if diamond_only and not journal.is_diamond_oa:
                continue

            # Construir conjunto de términos clave de la revista
            journal_text_pool = [journal.title] + journal.disciplines + journal.focus_keywords
            normalized_journal_tokens = set()
            for item in journal_text_pool:
                for w in extract_content_words(item):
                    normalized_journal_tokens.add(w)

            # 1. Coincidencia por bolsa de palabras (Jaccard ponderado)
            intersection = query_words.intersection(normalized_journal_tokens)
            if not intersection:
                continue

            jaccard_base = len(intersection) / len(query_words.union(normalized_journal_tokens))

            # 2. Ponderador por coincidencia de términos compuestos específicos
            phrase_bonus = 0.0
            for kw in journal.focus_keywords:
                norm_kw = normalize_token(kw)
                if norm_kw in text_norm:
                    phrase_bonus += 0.15

            # Score final acotado entre 0.0 y 1.0
            raw_score = min(1.0, (jaccard_base * 2.5) + phrase_bonus)

            if raw_score >= min_score:
                scored_results.append({
                    "journal": journal,
                    "score": round(raw_score, 3),
                    "confidence_pct": round(raw_score * 100, 1),
                    "matched_terms": sorted(list(intersection)),
                })

        # Ordenar descendentemente por score
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:top_n]

    def aggregate_authors_from_works(
        self, works: List[Dict[str, Any]], top_n: int = 5
    ) -> List[Dict[str, Any]]:
        """Agrupa y cuenta autores a partir de un listado de obras afines recuperadas."""
        author_counter: Dict[str, Dict[str, Any]] = {}

        for w in works:
            authorships = w.get("authorships") or []
            source_info = w.get("primary_location", {}).get("source", {})
            journal_title = source_info.get("display_name", "Revista no especificada")

            for auth in authorships:
                author_data = auth.get("author") or {}
                name = author_data.get("display_name")
                if not name:
                    continue

                institutions = auth.get("institutions") or []
                country = None
                if institutions:
                    country = institutions[0].get("country_code")

                if name not in author_counter:
                    author_counter[name] = {
                        "name": name,
                        "occurrences": 0,
                        "country": country,
                        "journals": set(),
                    }

                author_counter[name]["occurrences"] += 1
                if journal_title:
                    author_counter[name]["journals"].add(journal_title)

        ranked = []
        for name, data in author_counter.items():
            ranked.append({
                "name": data["name"],
                "occurrences": data["occurrences"],
                "country": data["country"],
                "journals": sorted(list(data["journals"])),
            })

        ranked.sort(key=lambda x: x["occurrences"], reverse=True)
        return ranked[:top_n]

    def fetch_live_reviewers(
        self,
        text: str,
        target_issns: Optional[List[str]] = None,
        max_works: int = 25,
        top_n: int = 5,
    ) -> List[Dict[str, Any]]:
        """Consulta OpenAlex en vivo para encontrar autores que han publicado recientemente
        en las revistas objetivo sobre temas afines.
        """
        words = extract_content_words(text)
        if not words:
            return []

        # Ordenar por longitud descendente para priorizar términos sustantivos específicos
        sorted_terms = sorted([w for w in set(words) if len(w) >= 4], key=len, reverse=True)
        if not sorted_terms:
            sorted_terms = words[:2]

        filter_parts = ["type:article"]
        if target_issns:
            # OpenAlex exige ISSNs con guión (ej. 0717-6996)
            formatted_issns = []
            for issn in target_issns:
                raw = issn.strip().replace(" ", "")
                if len(raw) == 8 and "-" not in raw:
                    formatted_issns.append(f"{raw[:4]}-{raw[4:]}")
                elif "-" in raw:
                    formatted_issns.append(raw)
            if formatted_issns:
                filter_parts.append("locations.source.issn:" + "|".join(formatted_issns))

        filter_expr = ",".join(filter_parts)

        # Probar con los primeros términos informativos hasta obtener resultados
        for query_candidate in sorted_terms[:3]:
            try:
                data = fetch_openalex_page(
                    filter_expr=filter_expr,
                    search_query=query_candidate,
                    per_page=min(max_works, 30),
                )
                works = data.get("results") or []
                if works:
                    return self.aggregate_authors_from_works(works, top_n=top_n)
            except Exception:
                continue

        return []


def generate_match_report(
    text_query: str,
    journal_matches: List[Dict[str, Any]],
    author_matches: Optional[List[Dict[str, Any]]] = None,
) -> str:
    """Genera un reporte estructurado en Markdown con las recomendaciones de revistas y revisores."""
    lines = [
        "# Reporte de Coincidencia de Revistas (JANE Latam)",
        "",
        "**Herramienta:** Investigadopedia Match v1.0.0 (Ciencias Sociales y Humanidades Iberoamérica)",
        "**Modelo de indexación:** Acceso Abierto Diamante (SciELO, Redalyc, Latindex Catálogo 2.0)",
        "",
        "### Extracto de Consulta Evaluado",
        f"> {text_query[:300]}..." if len(text_query) > 300 else f"> {text_query}",
        "",
        "---",
        "",
        "## Revistas Sugeridas",
        "",
        "| Ranking | Revista | País | Afinidad | Indexación | Acceso | ISSN |",
        "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |",
    ]

    for idx, match in enumerate(journal_matches, start=1):
        j: LatamJournal = match["journal"]
        index_badges = ", ".join(k.upper() for k in j.indexing)
        oa_status = "Diamante (Sin APC)" if j.is_diamond_oa else "APC / Tradicional"
        lines.append(
            f"| {idx} | **{j.title}** | {j.country} | {match['confidence_pct']}% | {index_badges} | {oa_status} | `{j.issn}` |"
        )

    lines.append("")
    lines.append("### Detalle de Coincidencias Temáticas")
    for idx, match in enumerate(journal_matches, start=1):
        j: LatamJournal = match["journal"]
        terms = ", ".join(match["matched_terms"])
        lines.append(f"- **{idx}. {j.title}**:")
        lines.append(f"  - Institución: *{j.publisher}*")
        lines.append(f"  - Términos coincidentes: `{terms}`")
        if j.url:
            lines.append(f"  - Sitio web: [{j.url}]({j.url})")

    if author_matches:
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## Autores y Revisores Potenciales Sugeridos")
        lines.append("")
        lines.append("Investigadores con publicaciones recientes afines en la región:")
        lines.append("")
        lines.append("| Autor | País | Obras Afines | Revistas Donde Publica |")
        lines.append("| :--- | :--- | :--- | :--- |")
        for auth in author_matches:
            country = auth.get("country") or "N/D"
            journals = ", ".join(auth.get("journals", []))
            lines.append(f"| **{auth['name']}** | {country} | {auth['occurrences']} | {journals} |")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("### Resguardo Metodológico e Integridad")
    lines.append("- Todas las revistas priorizadas forman parte del ecosistema público latinoamericano (SciELO / Redalyc / Latindex 2.0).")
    lines.append("- No se incluyen revistas depredadoras ni modelos comerciales cerrados con altas barreras de APC.")
    lines.append("")

    return "\n".join(lines)
