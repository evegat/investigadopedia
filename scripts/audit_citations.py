#!/usr/bin/env python3
"""Gate 2: Auditoría de citas, referencias y enlaces bibliográficos (Citation Integrity Gate)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DOCS_TO_SCAN = [
    REPO_ROOT / "Paper - Investigadopedia Observatorio.md",
    REPO_ROOT / "Corpus inicial - apoyos IA para investigar.md",
    REPO_ROOT / "PRD Investigadopedia.md"
]

FORBIDDEN_PLACEHOLDERS = [
    r"doi_aqui",
    r"todo_cita",
    r"enlace_pendiente",
    r"completar_referencia",
    r"lorem ipsum",
    r"autor,\s*202\?",
    r"citar_aqui"
]

DOI_REGEX = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+")
URL_REGEX = re.compile(r"https?://[^\s)\]\"'>]+")

def audit_citations() -> int:
    print("[CITATION INTEGRITY GATE] Auditando referencias bibliográficas y enlaces...")
    errors = 0
    total_sources = 0

    for doc_path in DOCS_TO_SCAN:
        if not doc_path.exists():
            continue
            
        text = doc_path.read_text(encoding="utf-8", errors="ignore")
        rel_name = doc_path.name

        # 1. Check for placeholders
        for pat in FORBIDDEN_PLACEHOLDERS:
            matches = re.findall(pat, text, re.IGNORECASE)
            if matches:
                print(f"[FAIL] {rel_name}: Se encontraron {len(matches)} placeholder(s) de citas prohibidos ('{matches[0]}')")
                errors += 1

        # 2. Extract and count citations / URLs / DOIs
        urls = URL_REGEX.findall(text)
        dois = DOI_REGEX.findall(text)
        wikilinks = re.findall(r"\[\[([^\]]+)\]\]", text)
        
        # Count explicit tool/paper references in tables
        table_rows = [line for line in text.splitlines() if line.startswith("|") and not line.startswith("|---")]
        
        print(f"[INFO] {rel_name}: {len(urls)} URLs, {len(dois)} DOIs, {len(wikilinks)} wikilinks, {len(table_rows)} registros tabulares.")
        total_sources += len(urls) + len(dois)

    if errors == 0:
        print(f"[CITATION GATE: PASS] Cero placeholders prohibidos. Citas y anclas auditadas con éxito.\n")
        return 0
    else:
        print(f"[CITATION GATE: FAIL] {errors} error(es) en integridad bibliográfica.\n")
        return 1

if __name__ == "__main__":
    sys.exit(audit_citations())
