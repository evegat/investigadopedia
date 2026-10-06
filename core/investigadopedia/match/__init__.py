"""
Módulo Match para Investigadopedia: Recomendador y estimador de revistas y autores
especializado en Ciencias Sociales y Humanidades para América Latina y el Caribe (JANE Latam).
"""

from .scramble import scramble_text
from .catalog import LatamJournal, get_latam_social_science_journals
from .estimator import JournalEstimator, generate_match_report

__all__ = [
    "scramble_text",
    "LatamJournal",
    "get_latam_social_science_journals",
    "JournalEstimator",
    "generate_match_report",
]
