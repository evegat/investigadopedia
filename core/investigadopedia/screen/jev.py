"""
Módulo de cribado acelerado con TypeSafe Jev (System 1 RLCD) para Investigadopedia.
Aprovecha la latencia ultra-baja (70-500ms) y costo mínimo ($0.042/1M tokens) de Jev
para cribar masivamente miles de abstracts según criterios de inclusión/exclusión PRISMA.
Incluye fallback heurístico determinista si no se dispone de credenciales de Jev.
"""

import json
import os
import urllib.request
from typing import Dict, List, Any, Optional


class JevClassifier:
    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None):
        self.api_key = api_key or os.getenv("JEV_API_KEY")
        self.endpoint = endpoint or os.getenv("JEV_ENDPOINT", "https://api.typesafe.ai/v1/decide")

    def screen_paper(self, title: str, abstract: Optional[str], criteria: str) -> Dict[str, Any]:
        """Evalúa un paper contra criterios de inclusión/exclusión."""
        abstract_text = abstract or "Sin abstract disponible"
        prompt_text = f"Criterios de inclusión: {criteria}\n\nTítulo: {title}\nAbstract: {abstract_text}"

        # Si tenemos credenciales de Jev en el entorno
        if self.api_key:
            try:
                payload = {
                    "model": "jev-latest",
                    "input": prompt_text,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "include": {"type": "boolean"},
                            "confidence": {"type": "number"},
                            "reason": {"type": "string"},
                        },
                        "required": ["include", "confidence", "reason"],
                    },
                }
                req = urllib.request.Request(
                    self.endpoint,
                    data=json.dumps(payload).encode("utf-8"),
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                )
                with urllib.request.urlopen(req, timeout=10) as resp:
                    if resp.status == 200:
                        return json.loads(resp.read().decode("utf-8"))
            except Exception:
                pass  # Fallback a heurística

        # Heurística determinista local (Fallback seguro sin internet ni keys)
        criteria_words = set(criteria.lower().split())
        content_words = set((title + " " + abstract_text).lower().split())
        intersection = criteria_words.intersection(content_words)
        match_ratio = len(intersection) / max(1, len(criteria_words))
        
        is_relevant = match_ratio > 0.15 or len(intersection) >= 2
        return {
            "include": is_relevant,
            "confidence": round(min(1.0, match_ratio * 2), 2),
            "reason": f"Coincidencia de términos clave ({len(intersection)} términos encontrados: {list(intersection)[:4]}) [Heurística Local]",
        }
