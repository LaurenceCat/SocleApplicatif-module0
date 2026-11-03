"""Module d'analyse de sentiment base sur NLTK VADER (baseline lexicale M0)."""

from typing import Dict, Any
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from iatos_core.logger import logger


class SentimentAnalyzer:
    """Analyseur de sentiment utilisant NLTK VADER."""

    def __init__(self):
        self._ensure_lexicon()
        self.sia = SentimentIntensityAnalyzer()
        logger.info("SentimentIntensityAnalyzer NLTK initialise.")

    def _ensure_lexicon(self):
        try:
            nltk.data.find("sentiment/vader_lexicon.zip")
        except LookupError:
            logger.info("Telechargement automatique de 'vader_lexicon'...")
            nltk.download("vader_lexicon", quiet=True)

    def analyze(self, texte: str) -> Dict[str, Any]:
        """Analyse la polarite d'un texte donne.
        
        Args:
            texte: Texte ou avis client a analyser.
            
        Returns:
            Dictionnaire avec le score compound, le label et les scores elementaires.
        """
        texte_clean = texte.strip()
        if not texte_clean:
            logger.warning("Texte vide transmis pour l'analyse de sentiment.")
            return {
                "texte": "",
                "compound": 0.0,
                "label": "Neutre",
                "scores": {"neg": 0.0, "neu": 1.0, "pos": 0.0, "compound": 0.0},
                "type_modele": "NLTK VADER (Baseline Lexicale M0)",
            }

        scores = self.sia.polarity_scores(texte_clean)
        compound = scores["compound"]

        if compound >= 0.05:
            label = "Positif"
        elif compound <= -0.05:
            label = "Negatif"
        else:
            label = "Neutre"

        logger.info("Analyse de sentiment pour '{t}...' : compound={c:.3f} ({l})", t=texte_clean[:30], c=compound, l=label)

        return {
            "texte": texte_clean,
            "compound": compound,
            "label": label,
            "scores": scores,
            "type_modele": "NLTK VADER (Baseline Lexicale M0)",
        }
