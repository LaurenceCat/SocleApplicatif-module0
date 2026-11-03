"""Tests unitaires pour les composants ML et NLP."""

from iatos_core.ml.scoring import CreditScoringPredictor
from iatos_core.ml.sentiment import SentimentAnalyzer


def test_credit_scoring_predictor():
    predictor = CreditScoringPredictor()
    
    # Cas 1 : Profil solide (Revenu eleve, petit montant, courte duree)
    res_favorable = predictor.predict(
        montant_demande=5000.0,
        duree_mois=12,
        revenu_mensuel=6000.0,
    )
    assert 300.0 <= res_favorable["score"] <= 850.0
    assert res_favorable["decision"] in ["Favorable", "Ajourne / Examen Approfondi"]
    assert "features_utilisees" in res_favorable

    # Cas 2 : Profil risque (Petit revenu, gros montant, longue duree)
    res_defavorable = predictor.predict(
        montant_demande=45000.0,
        duree_mois=84,
        revenu_mensuel=1200.0,
    )
    assert 300.0 <= res_defavorable["score"] <= 850.0
    assert res_defavorable["score"] < res_favorable["score"]


def test_sentiment_analyzer():
    analyzer = SentimentAnalyzer()

    # Cas positif
    res_pos = analyzer.analyze("This software is amazing, super fast and very reliable!")
    assert res_pos["label"] == "Positif"
    assert res_pos["compound"] >= 0.05

    # Cas negatif
    res_neg = analyzer.analyze("Horrible bug, complete loss of data, very disappointed.")
    assert res_neg["label"] == "Negatif"
    assert res_neg["compound"] <= -0.05

    # Cas vide
    res_empty = analyzer.analyze("")
    assert res_empty["label"] == "Neutre"
    assert res_empty["compound"] == 0.0
