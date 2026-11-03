"""Module de scoring de credit utilisant la regression lineaire baseline."""

from pathlib import Path
from typing import Dict, Any
import joblib
import pandas as pd
from iatos_core.config import CREDIT_MODEL_PATH
from iatos_core.logger import logger


class CreditScoringPredictor:
    """Predictor encapsulant le modele de regression lineaire pour le scoring de credit."""

    def __init__(self, model_path: Path = CREDIT_MODEL_PATH):
        self.model_path = model_path
        self._bundle = None
        self._model = None
        self._features = None
        self._load_model()

    def _load_model(self):
        if not self.model_path.exists():
            logger.warning("Fichier modele introuvable a {p}. Tentative d'entrainement a la volee...", p=self.model_path)
            from data.train_baseline import train_baseline
            self._bundle = train_baseline()
        else:
            self._bundle = joblib.load(self.model_path)

        self._model = self._bundle["model"]
        self._features = self._bundle["features"]
        logger.info("Modele de scoring charge : features={f}", f=self._features)

    def predict(self, montant_demande: float, duree_mois: int, revenu_mensuel: float) -> Dict[str, Any]:
        """Predire le score de credit a partir des 3 attributs financiers neutres.
        
        Args:
            montant_demande: Montant du pret en euros.
            duree_mois: Duree du pret en mois.
            revenu_mensuel: Revenu mensuel net de l'emprunteur.
            
        Returns:
            Dictionnaire avec le score predit, la decision et les metadonnees.
        """
        logger.info("Scoring en cours : montant={m}E, duree={d}m, revenu={r}E", m=montant_demande, d=duree_mois, r=revenu_mensuel)

        df_input = pd.DataFrame([{
            "montant_demande": float(montant_demande),
            "duree_mois": int(duree_mois),
            "revenu_mensuel": float(revenu_mensuel),
        }])

        raw_score = float(self._model.predict(df_input)[0])
        # Borner entre 300 et 850 (standard FICO / scoring bancaire)
        clamped_score = round(max(300.0, min(850.0, raw_score)), 1)

        # Regle de decision indicative
        if clamped_score >= 650.0:
            decision = "Favorable"
            motif = "Profil solide avec capacite de remboursement estimee satisfaisante."
        elif clamped_score >= 550.0:
            decision = "Ajourne / Examen Approfondi"
            motif = "Profil intermediaire necessitant l'analyse de garanties complementaires."
        else:
            decision = "Defavorable"
            motif = "Tension financiere detectee par rapport au montant et a la duree sollicites."

        logger.info("Resultat scoring : score={s} -> decision='{dec}'", s=clamped_score, dec=decision)

        return {
            "score": clamped_score,
            "decision": decision,
            "motif": motif,
            "features_utilisees": {
                "montant_demande": montant_demande,
                "duree_mois": duree_mois,
                "revenu_mensuel": revenu_mensuel,
            },
            "type_modele": "Regression Lineaire Scikit-Learn (Baseline M0)",
        }
