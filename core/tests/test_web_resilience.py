"""
Pruebas de regresión unitarias para el blindaje de resiliencia y privacidad de Investigadopedia Web.
TDD: Verifica resguardo de privacidad (zero-knowledge queries), sanitización y catálogo offline.
"""

import json
import unittest
from pathlib import Path
from investigadopedia.match.estimator import extract_content_words
from investigadopedia.match.catalog import get_latam_social_science_journals


class TestWebPrivacyAndResilience(unittest.TestCase):

    def test_journals_json_exists_and_offline_capable(self):
        """Verifica que el catálogo JSON para la web exista y sea íntegro sin depender de red."""
        json_path = Path("web/data/journals.json")
        if not json_path.exists():
            json_path = Path("2 - Project/EDI001 - Investigadopedia/web/data/journals.json")
        self.assertTrue(json_path.exists(), "El archivo web/data/journals.json debe existir para servir offline.")
        data = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(data), 20)
        # Todos deben ser Diamante por política editorial
        for j in data:
            self.assertTrue(j["is_diamond_oa"])
            self.assertTrue(len(j["focus_keywords"]) > 0)

    def test_query_sanitization_zero_knowledge(self):
        """Verifica que nunca se envíe una oración completa a APIs externas, solo términos aislados."""
        confidential_draft = (
            "En esta investigación inédita demostramos que el algoritmo propietario X "
            "implementado en el hospital de Santiago redujo la mortalidad en un 15%."
        )
        words = extract_content_words(confidential_draft)
        # Verificar que stopwords y estructura gramatical queden completamente destruidas
        self.assertNotIn("demostramos", words)
        self.assertNotIn("esta", words)
        self.assertNotIn("en", words)
        # El término que se enviaría a una API como query debe ser máximo de 1-2 palabras aisladas
        safe_search_term = words[0] if words else ""
        self.assertTrue(len(safe_search_term.split()) == 1)
        self.assertNotIn("algoritmo propietario X implementado", safe_search_term)

    def test_sanitize_html_utility(self):
        """Verifica la lógica de neutralización de inyecciones XSS."""
        from investigadopedia.match.scramble import sanitize_html_text
        malicious_input = '<script>alert("hack")</script><b>Estudio</b> sobre políticas'
        cleaned = sanitize_html_text(malicious_input)
        self.assertNotIn("<script>", cleaned)
        self.assertNotIn("</script>", cleaned)
        self.assertIn("&lt;script&gt;", cleaned)

    def test_roadmap_proposals_sanitization(self):
        """Verifica que las propuestas de usuarios enviadas al roadmap se saniticen."""
        from investigadopedia.match.scramble import sanitize_html_text
        user_suggestion = "Agregar revista <a href='evil.com'>Revista Falsa</a> y filtro WoS"
        sanitized = sanitize_html_text(user_suggestion)
        self.assertNotIn("<a", sanitized)
        self.assertIn("&lt;a", sanitized)


if __name__ == "__main__":
    unittest.main()
