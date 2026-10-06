"""
Anonimización por Scramble (Inspirado en JANE).
Permuta y ordena alfabéticamente los términos de un abstract o título en el cliente local.
Permite mantener las frecuencias y n-gramas para motores basados en bolsas de palabras o embeddings
sin exponer la sintaxis ni el texto continuo legible del manuscrito inédito.
"""

import re


def scramble_text(text: str) -> str:
    """Desordena y ordena alfabéticamente las palabras de un texto.

    Separa por espacios y puntuaciones comunes, normaliza a minúsculas,
    ordena alfabéticamente y une con espacios simples.
    """
    if not text:
        return ""
    # Separar por delimitadores comunes
    tokens = re.split(r"[ \t\n\r.,;:()\[\]{}'\"!?¿¡/\\-]+", text)
    cleaned = [t.lower() for t in tokens if t.strip()]
    cleaned.sort()
    return " ".join(cleaned)


def sanitize_html_text(text: str) -> str:
    """Escapa caracteres peligrosos en texto plano para prevenir inyecciones HTML/XSS."""
    if not text:
        return ""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )
