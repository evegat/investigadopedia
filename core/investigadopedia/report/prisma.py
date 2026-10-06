"""
Generador de Diagrama de Flujo y Reporte PRISMA 2020 para Investigadopedia.
Produce especificaciones Mermaid y Markdown estructuradas para manuscritos.
"""

from typing import Dict, Any


def generate_prisma_markdown(
    identified_counts: Dict[str, int],
    duplicates_removed: int,
    screened_count: int,
    excluded_screening: int,
    full_text_assessed: int,
    excluded_full_text: int,
    included_count: int,
) -> str:
    """Genera la sección de reporte y diagrama Mermaid PRISMA 2020."""
    total_identified = sum(identified_counts.values())

    sources_str = "\n".join([f"        - {k}: {v}" for k, v in identified_counts.items()])

    mermaid_diagram = f"""```mermaid
flowchart TD
    subgraph IDENTIFICACION["1. Identificación"]
        A["Registros identificados en bases de datos<br>(n = {total_identified})"]
        B["Registros duplicados removidos<br>(n = {duplicates_removed})"]
        A --> B
    end

    subgraph CRIBADO["2. Cribado (Screening)"]
        C["Registros cribados por título/abstract<br>(n = {screened_count})"]
        D["Registros excluidos por criterios<br>(n = {excluded_screening})"]
        B --> C
        C --> D
    end

    subgraph ELEGIBILIDAD["3. Elegibilidad"]
        E["Informes evaluados a texto completo<br>(n = {full_text_assessed})"]
        F["Informes excluidos a texto completo<br>(n = {excluded_full_text})"]
        C --> E
        E --> F
    end

    subgraph INCLUSION["4. Inclusión"]
        G["Estudios incluidos en la revisión<br>(n = {included_count})"]
        E --> G
    end
```"""

    report_md = f"""# Reporte de Flujo PRISMA 2020

## 1. Identificación
- **Total de registros identificados:** {total_identified}
{sources_str}
- **Duplicados removidos (DOI / Título normalizado):** {duplicates_removed}

## 2. Cribado (Screening)
- **Registros evaluados (título + abstract):** {screened_count}
- **Registros excluidos:** {excluded_screening}

## 3. Elegibilidad e Inclusión
- **Artículos evaluados a texto completo:** {full_text_assessed}
- **Artículos excluidos:** {excluded_full_text}
- **Estudios incluidos finalmente:** {included_count}

---

## Diagrama de Flujo PRISMA

{mermaid_diagram}
"""
    return report_md
