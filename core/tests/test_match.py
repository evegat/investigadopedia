"""
Pruebas de regresión unitarias para el módulo Match (JANE Latam Ciencias Sociales).
TDD: Verifica matching de revistas, anonimización por scramble y agregación de revisores.
"""

import unittest
from investigadopedia.match.scramble import scramble_text
from investigadopedia.match.catalog import get_latam_social_science_journals, LatamJournal
from investigadopedia.match.estimator import JournalEstimator, generate_match_report


class TestMatchModule(unittest.TestCase):

    def test_scramble_text(self):
        text = "Evaluación de políticas públicas en América Latina y cohesión social."
        scrambled = scramble_text(text)
        # El scramble debe contener las mismas palabras ordenadas alfabéticamente
        self.assertNotEqual(text, scrambled)
        words_original = sorted([w.lower().strip(".,;:()") for w in text.split() if w.strip(".,;:()")])
        words_scrambled = scrambled.split()
        self.assertEqual(words_original, words_scrambled)

    def test_catalog_entries(self):
        journals = get_latam_social_science_journals()
        self.assertGreaterEqual(len(journals), 10)
        # Verificar que revistas emblemáticas estén presentes y tipificadas
        eure = next((j for j in journals if "EURE" in j.title or "0717-6996" in j.issn), None)
        self.assertIsNotNone(eure)
        self.assertTrue(eure.is_diamond_oa)
        self.assertIn("scielo", eure.indexing)

    def test_offline_journal_matching(self):
        estimator = JournalEstimator()
        abstract = (
            "Este artículo analiza las políticas públicas urbanas y la segregación residencial "
            "en Santiago de Chile y Buenos Aires, evaluando la gobernanza metropolitana y vivienda social."
        )
        matches = estimator.match_journals(text=abstract, top_n=5, diamond_only=True)
        self.assertGreater(len(matches), 0)
        top_match = matches[0]
        self.assertIn("journal", top_match)
        self.assertGreater(top_match["score"], 0.0)
        # EURE o revistas de estudios urbanos/territoriales/políticas deben rankear alto
        titles = [m["journal"].title.lower() for m in matches]
        self.assertTrue(any("eure" in t or "política" in t or "urbano" in t or "social" in t for t in titles))

    def test_author_estimator_from_works(self):
        estimator = JournalEstimator()
        sample_works = [
            {
                "title": "Gobernanza urbana",
                "authorships": [
                    {"author": {"display_name": "Valenzuela, Pedro"}, "institutions": [{"country_code": "CL"}]},
                    {"author": {"display_name": "Soto, Marcela"}, "institutions": [{"country_code": "CL"}]}
                ],
                "primary_location": {"source": {"display_name": "EURE"}}
            },
            {
                "title": "Vivienda social en Chile",
                "authorships": [
                    {"author": {"display_name": "Valenzuela, Pedro"}, "institutions": [{"country_code": "CL"}]}
                ],
                "primary_location": {"source": {"display_name": "Revista INVI"}}
            }
        ]
        authors = estimator.aggregate_authors_from_works(sample_works)
        self.assertEqual(authors[0]["name"], "Valenzuela, Pedro")
        self.assertEqual(authors[0]["occurrences"], 2)

    def test_generate_match_report_markdown(self):
        estimator = JournalEstimator()
        abstract = "Análisis del gasto público en educación superior y desigualdad social."
        matches = estimator.match_journals(text=abstract, top_n=3)
        report = generate_match_report(
            text_query=abstract,
            journal_matches=matches,
            author_matches=[{"name": "Dra. Lucía Lagos", "occurrences": 3, "country": "CL", "journals": ["Perfiles Educativos"]}]
        )
        self.assertIn("# Reporte de Coincidencia de Revistas (JANE Latam)", report)
        self.assertIn("Revistas Sugeridas", report)
        self.assertIn("Acceso Abierto Diamante", report)

    def test_fetch_live_reviewers_mocked(self):
        from unittest.mock import patch
        estimator = JournalEstimator()
        mock_response = {
            "results": [
                {
                    "title": "Segregación y vivienda social",
                    "authorships": [
                        {"author": {"display_name": "Dra. Carolina Tohá"}, "institutions": [{"country_code": "CL"}]}
                    ],
                    "primary_location": {"source": {"display_name": "EURE"}}
                }
            ]
        }
        with patch("investigadopedia.match.estimator.fetch_openalex_page", return_value=mock_response):
            reviewers = estimator.fetch_live_reviewers(
                text="vivienda social y segregacion",
                target_issns=["0717-6996"],
                max_works=5
            )
            self.assertEqual(len(reviewers), 1)
            self.assertEqual(reviewers[0]["name"], "Dra. Carolina Tohá")
            self.assertEqual(reviewers[0]["country"], "CL")


if __name__ == "__main__":
    unittest.main()
