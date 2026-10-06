"""
Módulo de Vigilancia Epistemológica para Investigadopedia.
Valida la estricta distinción entre:
1. Hecho Observado (dato primario, cita verificable, registro medido)
2. Inferencia Fundada (deducción lógica derivada de hechos)
3. Supuesto / Brecha (hipótesis o ausencia de dato empírico)
"""

import re
from typing import Dict, List, Any


EPISTEMIC_LABELS = {
    "hecho": [r"\bhecho observado\b", r"\bdato primario\b", r"\bregistro administrativo\b", r"\bmedición empírica\b"],
    "inferencia": [r"\binferencia fundada\b", r"\bse infiere que\b", r"\bdeducción analítica\b", r"\blos datos sugieren\b"],
    "supuesto": [r"\bsupuesto\b", r"\bbrecha\b", r"\bhipótesis no contrastada\b", r"\blimitación\b"],
}


def audit_epistemic_text(text: str) -> Dict[str, Any]:
    """Audita un texto académico verificando el cumplimiento de la tripartición epistemológica."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip() and not p.strip().startswith("#")]
    
    labeled_counts = {"hecho": 0, "inferencia": 0, "supuesto": 0, "unlabeled": 0}
    findings = []

    for i, para in enumerate(paragraphs, 1):
        matched_types = []
        for cat, patterns in EPISTEMIC_LABELS.items():
            for pat in patterns:
                if re.search(pat, para, re.IGNORECASE):
                    matched_types.append(cat)
                    break

        if matched_types:
            for m in set(matched_types):
                labeled_counts[m] += 1
        else:
            labeled_counts["unlabeled"] += 1
            if len(para) > 120 and ("concluimos" in para.lower() or "demuestra que" in para.lower() or "es evidente" in para.lower()):
                findings.append({
                    "paragraph_index": i,
                    "excerpt": para[:140] + "...",
                    "issue": "Afirmación asertiva/conclusiva sin rotulación epistemológica explícita (riesgo de inferencia disfrazada de hecho).",
                })

    total = len(paragraphs)
    score = round(((total - len(findings)) / max(1, total)) * 100, 1)

    return {
        "total_paragraphs": total,
        "labeled_counts": labeled_counts,
        "compliance_score": score,
        "findings": findings,
        "status": "PASS" if score >= 80 and len(findings) == 0 else "REVIEW_REQUIRED",
    }
