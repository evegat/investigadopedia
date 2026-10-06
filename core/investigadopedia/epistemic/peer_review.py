"""
Módulo de Simulación de Arbitraje por Pares (Peer-Review Evaluator) para Investigadopedia.
Inspirado en las directrices editoriales de revisión de manuscritos de la Dra. Naureen Aleem (2026):
Audita un manuscrito académico contra los 7 ejes críticos evaluados por revisores de revistas científicas:
1. Relevancia e impacto (Significance)
2. Originalidad y brecha de literatura
3. Coherencia del marco teórico
4. Rigor metodológico y replicabilidad
5. Solidez del análisis empírico y consistencia de datos
6. Discusión, contraste y declaración de limitaciones
7. Calidad de redacción, estructura y referencias verificables
"""

import re
from pathlib import Path
from typing import Dict, List, Any


REVIEW_DIMENSIONS = [
    {
        "id": "significance",
        "name": "1. Importancia y Contribución (Significance)",
        "description": "¿El estudio aborda un problema relevante? ¿Aporta a teoría, práctica o política pública?",
        "keywords": ["problema", "contribución", "aporte", "relevancia", "política pública", "importancia"],
    },
    {
        "id": "literature_gap",
        "name": "2. Estado del Arte y Brecha (Literature Gap)",
        "description": "¿Identifica una brecha de conocimiento real en la literatura existente?",
        "keywords": ["brecha", "literatura", "estado del arte", "estudios previos", "antecedentes"],
    },
    {
        "id": "methodology",
        "name": "3. Metodología y Replicabilidad (Methodology)",
        "description": "¿El diseño muestral/censal, fuentes y procedimientos son replicables y transparentes?",
        "keywords": ["metodología", "datos", "muestra", "censo", "corpus", "fuente", "procedimiento", "análisis"],
    },
    {
        "id": "empirical_findings",
        "name": "4. Resultados y Evidencia (Findings)",
        "description": "¿Los hallazgos se sustentan estrictamente en la evidencia sin especulación?",
        "keywords": ["resultados", "hallazgos", "evidencia", "análisis", "tabla", "gráfico"],
    },
    {
        "id": "discussion_limitations",
        "name": "5. Discusión y Limitaciones (Discussion & Limitations)",
        "description": "¿Se discuten las implicancias y se reconocen explícitamente las limitaciones?",
        "keywords": ["discusión", "limitaciones", "implicancias", "futuras investigaciones", "sesgo"],
    },
    {
        "id": "conclusions_actionability",
        "name": "6. Conclusiones y Accionabilidad",
        "description": "¿Las conclusiones responden a la pregunta de investigación inicial?",
        "keywords": ["conclusión", "conclusiones", "recomendaciones", "cierre"],
    },
    {
        "id": "referencing_ethics",
        "name": "7. Trazabilidad Bibliográfica y Ética",
        "description": "¿Citas verificables en formato canónico (DOI) y transparencia de datos?",
        "keywords": ["referencias", "bibliografía", "doi", "datos abiertos", "repositorio"],
    },
]


def evaluate_manuscript_peer_review(text: str) -> Dict[str, Any]:
    """Evalúa un texto de manuscrito contra los 7 ejes de arbitraje editorial."""
    text_lower = text.lower()
    total_words = len(text.split())

    dimension_results = []
    total_score = 0

    for dim in REVIEW_DIMENSIONS:
        matches = [kw for kw in dim["keywords"] if kw in text_lower]
        has_section_header = any(
            re.search(rf"^#+\s*.*{kw}", text, re.IGNORECASE | re.MULTILINE)
            for kw in dim["keywords"]
        )

        # Puntuación preliminar (0 a 10)
        score = 0
        if has_section_header:
            score += 5
        score += min(5, len(matches))

        total_score += score
        dimension_results.append({
            "dimension": dim["name"],
            "description": dim["description"],
            "score": score,
            "max_score": 10,
            "has_dedicated_section": has_section_header,
            "matched_signals": matches[:5],
            "status": "PASS" if score >= 6 else "NEEDS_ATTENTION",
        })

    average_percentage = round((total_score / (len(REVIEW_DIMENSIONS) * 10)) * 100, 1)

    recommendation = (
        "ACCEPT_WITH_MINOR_REVISIONS" if average_percentage >= 80 else
        "MAJOR_REVISIONS_REQUIRED" if average_percentage >= 50 else
        "REJECT_STRUCTURAL_GAPS"
    )

    return {
        "total_words": total_words,
        "overall_readiness_score": average_percentage,
        "editorial_recommendation": recommendation,
        "dimensions": dimension_results,
    }


def generate_peer_review_report(eval_data: Dict[str, Any], filename: str) -> str:
    """Genera un informe estructurado de revisión por pares en Markdown."""
    lines = [
        f"# Informe de Arbitraje Editorial Simulado — {filename}",
        f"\n**Dictamen Editorial:** `{eval_data['editorial_recommendation']}`",
        f"**Índice de Madurez para Envío:** {eval_data['overall_readiness_score']}%",
        f"**Extensión del manuscrito:** {eval_data['total_words']} palabras\n",
        "---",
        "\n## Evaluación por Dimensiones Críticas de Revisión\n",
    ]

    for dim in eval_data["dimensions"]:
        badge = "✅ CUMPLIDO" if dim["status"] == "PASS" else "⚠️ REVISAR"
        lines.append(f"### {dim['dimension']} — {badge}")
        lines.append(f"*{dim['description']}*")
        lines.append(f"- **Puntaje:** {dim['score']} / {dim['max_score']}")
        lines.append(f"- **Sección identificada:** {'Sí' if dim['has_dedicated_section'] else 'No explícita en encabezados'}")
        lines.append(f"- **Señales encontradas:** {', '.join(dim['matched_signals']) if dim['matched_signals'] else 'Ninguna detectada'}\n")

    lines.append("---\n*Generado por Investigadopedia Peer-Review Evaluator (v1.0.0)*")
    return "\n".join(lines)
