#!/usr/bin/env python3
"""Gate 1: Verificador de integridad y procedencia de datos crudos (Sourcing Gate)."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = REPO_ROOT / "data" / "raw"
MANIFEST_PATH = RAW_DIR / "manifest.json"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest().lower()

def verify_sourcing() -> int:
    print("[SOURCING GATE] Verificando proveniencia e integridad en data/raw...")
    
    if not MANIFEST_PATH.exists():
        print(f"[FAIL] No existe el manifiesto de datos en {MANIFEST_PATH}")
        return 1
        
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"[FAIL] Error leyendo manifest.json: {exc}")
        return 1

    files_declared = manifest.get("files", [])
    if not files_declared:
        print("[FAIL] manifest.json no declara archivos.")
        return 1

    manifested_names = set()
    errors = 0

    for item in files_declared:
        fname = item.get("filename")
        expected_hash = item.get("sha256", "").lower()
        manifested_names.add(fname)
        
        file_path = RAW_DIR / fname
        if not file_path.exists():
            print(f"[FAIL] Archivo declarado ausente: {fname}")
            errors += 1
            continue

        real_hash = sha256_file(file_path)
        if real_hash != expected_hash:
            print(f"[FAIL] Hash divergente en {fname}! Esperado: {expected_hash[:12]}..., Real: {real_hash[:12]}...")
            errors += 1
        else:
            print(f"[PASS] {fname} (SHA-256 verificado: {real_hash[:12]}...)")

    # Check for unmanifested raw files
    for raw_file in RAW_DIR.glob("*"):
        if raw_file.name != "manifest.json" and raw_file.name not in manifested_names:
            print(f"[WARN] Archivo no manifestado en data/raw: {raw_file.name}")

    if errors == 0:
        print("[SOURCING GATE: PASS] Todos los datasets crudos están íntegros y trazables.\n")
        return 0
    else:
        print(f"[SOURCING GATE: FAIL] {errors} error(es) detectado(s).\n")
        return 1

if __name__ == "__main__":
    sys.exit(verify_sourcing())
