#!/usr/bin/env python3
"""Orquestador de Gates del Research & Data Harness para Investigadopedia (EDI001)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# Force UTF-8 encoding on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')


REPO_ROOT = Path(__file__).resolve().parent.parent

GATES = [
    {
        "name": "Gate 1: Sourcing & Raw Integrity",
        "command": [sys.executable, str(REPO_ROOT / "scripts" / "verify_sourcing.py")]
    },
    {
        "name": "Gate 2: Citation & Reference Audit",
        "command": [sys.executable, str(REPO_ROOT / "scripts" / "audit_citations.py")]
    },
    {
        "name": "Gate 3: Data Sanity & Unit Tests",
        "command": [sys.executable, "-m", "unittest", "discover", "-s", str(REPO_ROOT / "tests"), "-p", "test_*.py"]
    }
]

def main() -> int:
    print("=" * 70)
    print("  RESEARCH & DATA HARNESS (EDI001 - Investigadopedia)")
    print("=" * 70 + "\n")

    failed = 0
    for gate in GATES:
        print(f"--> Ejecutando {gate['name']}...")
        res = subprocess.run(gate["command"], cwd=str(REPO_ROOT), capture_output=True, text=True, encoding="utf-8", errors="replace")
        
        if res.returncode == 0:
            print(f"[PASS] {gate['name']}")
            if res.stdout.strip():
                # Print last few lines of output
                lines = res.stdout.strip().splitlines()
                for line in lines[-4:]:
                    print(f"       {line}")
        else:
            print(f"[FAIL] {gate['name']} (exit={res.returncode})")
            if res.stdout:
                print(res.stdout)
            if res.stderr:
                print(res.stderr)
            failed += 1
        print("-" * 70)

    print("\n" + "=" * 70)
    if failed == 0:
        print("  RESULTADO GLOBAL: TODOS LOS GATES DE INVESTIGACIÓN APROBADOS [PASS]")
        print("=" * 70 + "\n")
        return 0
    else:
        print(f"  RESULTADO GLOBAL: {failed} GATE(S) FALLIDO(S) [FAIL]")
        print("=" * 70 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
