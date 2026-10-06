"""
Pruebas de regresión unitarias para Investigadopedia Core.
Verifica deduplicación no-Latin, partición física, tripartición epistemológica y PRISMA sin depender de internet.
"""

import json
import tempfile
import unittest
from pathlib import Path

from investigadopedia.screen.dedup import normalize_doi, normalize_title, merge_jsonl_files
from investigadopedia.screen.partition import partition_corpus
from investigadopedia.screen.jev import JevClassifier
from investigadopedia.epistemic.tripartition import audit_epistemic_text
from investigadopedia.report.prisma import generate_prisma_markdown


class TestInvestigadopediaCore(unittest.TestCase):

    def test_normalize_doi(self):
        self.assertEqual(normalize_doi("https://doi.org/10.1000/182"), "10.1000/182")
        self.assertEqual(normalize_doi("http://dx.doi.org/10.1000/182"), "10.1000/182")
        self.assertEqual(normalize_doi("doi: 10.1000/182"), "10.1000/182")
        self.assertIsNone(normalize_doi(None))

    def test_normalize_title_unicode_preservation(self):
        # Título en español con tildes
        t1 = normalize_title("Gestión Pública y Políticas Sociales: Una Revisión")
        t2 = normalize_title("gestion publica y politicas sociales una revision")
        self.assertEqual(t1, t2)
        
        # Preservación de caracteres no-latinos (cirílico)
        t_cyrillic = normalize_title("Искусственный Интеллект")
        self.assertTrue(len(t_cyrillic) > 0)
        self.assertEqual(t_cyrillic, "искусственный интеллект")

    def test_dedup_and_merge(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            file1 = Path(tmpdir) / "f1.jsonl"
            file2 = Path(tmpdir) / "f2.jsonl"
            out = Path(tmpdir) / "merged.jsonl"

            # Dos registros duplicados por DOI
            rec1 = {"doi": "10.1234/test", "title": "Paper Uno", "source_engine": "redalyc"}
            rec2 = {"doi": "https://doi.org/10.1234/test", "title": "Paper Uno Modificado", "source_engine": "scielo", "abstract": "Resumen completo"}
            # Un registro único por título
            rec3 = {"title": "Paper Distinto", "source_engine": "scielo"}

            file1.write_text(json.dumps(rec1) + "\n", encoding="utf-8")
            file2.write_text(json.dumps(rec2) + "\n" + json.dumps(rec3) + "\n", encoding="utf-8")

            total = merge_jsonl_files([str(file1), str(file2)], str(out))
            self.assertEqual(total, 2)

            merged_data = [json.loads(l) for l in out.read_text(encoding="utf-8").splitlines()]
            # Verificar fusión de fuentes
            twin = next(r for r in merged_data if r.get("doi") == "https://doi.org/10.1234/test" or r.get("doi") == "10.1234/test")
            self.assertIn("redalyc", twin["source_engines"])
            self.assertIn("scielo", twin["source_engines"])
            self.assertEqual(twin.get("abstract"), "Resumen completo")

    def test_partition_corpus(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            in_file = Path(tmpdir) / "input.jsonl"
            out_dir = Path(tmpdir) / "partition"

            records = [
                {"title": "Paper Arbitrado", "issn_l": "1234-5678", "venue": "Revista Científica"},
                {"title": "Preprint no arbitrado", "venue": "arXiv preprint", "issn_l": None},
                {"title": "x", "venue": "inválido"},  # dropped por título corto
            ]
            in_file.write_text("\n".join(json.dumps(r) for r in records), encoding="utf-8")

            rep = partition_corpus(str(in_file), str(out_dir))
            self.assertEqual(rep["academic_peer_reviewed"], 1)
            self.assertEqual(rep["grey_literature"], 1)
            self.assertEqual(rep["dropped_invalid"], 1)
            self.assertTrue((out_dir / "corpus_academic.jsonl").exists())

    def test_epistemic_tripartition(self):
        sample_text = (
            "## Resultados\n\n"
            "Dato primario: Se registraron 4.504 procesos en el período analizado.\n\n"
            "Se infiere que la mayoría de los procesos corresponden a equipamiento mecánico.\n\n"
            "Supuesto: No se cuenta con datos sobre precios unitarios en 2008.\n"
        )
        report = audit_epistemic_text(sample_text)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["compliance_score"], 100.0)
        self.assertEqual(report["labeled_counts"]["hecho"], 1)
        self.assertEqual(report["labeled_counts"]["inferencia"], 1)
        self.assertEqual(report["labeled_counts"]["supuesto"], 1)

    def test_prisma_markdown_generation(self):
        md = generate_prisma_markdown(
            identified_counts={"SciELO": 120, "Redalyc": 80},
            duplicates_removed=30,
            screened_count=170,
            excluded_screening=100,
            full_text_assessed=70,
            excluded_full_text=20,
            included_count=50,
        )
        self.assertIn("Total de registros identificados:** 200", md)
        self.assertIn("Estudios incluidos finalmente:** 50", md)
        self.assertIn("flowchart TD", md)

    def test_peer_review_evaluator(self):
        from investigadopedia.epistemic.peer_review import evaluate_manuscript_peer_review
        sample_manuscript = (
            "# Título del Paper\n\n"
            "## Introducción y Problema\nEl problema de investigación es la opacidad digital.\n\n"
            "## Estado del Arte\nExiste una brecha en la literatura previa sobre ordenanzas.\n\n"
            "## Metodología y Datos\nSe analizó un corpus censal de datos abiertos con procedimiento reproducible.\n\n"
            "## Resultados y Evidencia\nLos hallazgos muestran diferencias en la tabla 1.\n\n"
            "## Discusión y Limitaciones\nDiscutimos las implicancias y reconocemos el sesgo de conectividad.\n\n"
            "## Conclusiones\nLas recomendaciones finales aportan a la política pública.\n\n"
            "## Referencias\nDOI: 10.1234/test. Datos abiertos disponibles en el repositorio.\n"
        )
        res = evaluate_manuscript_peer_review(sample_manuscript)
        self.assertGreaterEqual(res["overall_readiness_score"], 70.0)
        self.assertEqual(res["editorial_recommendation"], "ACCEPT_WITH_MINOR_REVISIONS")
        self.assertEqual(len(res["dimensions"]), 7)


if __name__ == "__main__":
    unittest.main()
