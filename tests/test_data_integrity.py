#!/usr/bin/env python3
"""Gate 3: Pruebas unitarias de consistencia de datos y aserciones (Data Integrity Test)."""

import csv
import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_CSV = REPO_ROOT / "data" / "raw" / "herramientas_ia_corpus.csv"
OUTPUT_DIR = REPO_ROOT / "data" / "outputs"

ALLOWED_TYPES = {
    "agente_open_source",
    "saas_investigacion",
    "buscador_ia",
    "asistente_lectura",
    "mapa_literatura",
    "cuaderno_fuentes",
    "repo_open_source"
}

class TestDataIntegrity(unittest.TestCase):
    def setUp(self):
        self.assertTrue(RAW_CSV.exists(), f"Archivo crudo no encontrado: {RAW_CSV}")
        self.rows = []
        with RAW_CSV.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.rows.append(row)

    def test_minimum_records(self):
        """Verifica que el dataset contenga al menos 5 registros evaluados."""
        self.assertGreaterEqual(len(self.rows), 5, "El corpus inicial debe tener al menos 5 herramientas")

    def test_required_fields_not_empty(self):
        """Verifica que ninguna fila tenga columnas clave vacías."""
        for i, row in enumerate(self.rows):
            self.assertTrue(row.get("herramienta"), f"Fila {i}: herramienta vacía")
            self.assertTrue(row.get("tipo"), f"Fila {i}: tipo vacío")
            self.assertTrue(row.get("etapas"), f"Fila {i}: etapas vacías")
            self.assertTrue(row.get("riesgo_declarado"), f"Fila {i}: riesgo no declarado")

    def test_no_duplicate_tools(self):
        """Verifica unicidad en los nombres de herramientas."""
        names = [r["herramienta"].strip().lower() for r in self.rows]
        self.assertEqual(len(names), len(set(names)), "Existen nombres de herramientas duplicados")

    def test_allowed_types(self):
        """Verifica que las categorías correspondan a la taxonomía definida."""
        for row in self.rows:
            t = row["tipo"].strip()
            self.assertIn(t, ALLOWED_TYPES, f"Tipo inválido '{t}' en herramienta {row['herramienta']}")

    def test_reproducible_output_generation(self):
        """Verifica que se pueda compilar un output reproducible hacia data/outputs/."""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        summary = {
            "total_tools": len(self.rows),
            "by_type": {},
            "generated_by": "Gate 3 Reproducible Analysis"
        }
        for r in self.rows:
            t = r["tipo"].strip()
            summary["by_type"][t] = summary["by_type"].get(t, 0) + 1
            
        out_file = OUTPUT_DIR / "resumen_corpus.json"
        out_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
        self.assertTrue(out_file.exists(), "El archivo de salida reproducible no se generó")

if __name__ == "__main__":
    unittest.main()
