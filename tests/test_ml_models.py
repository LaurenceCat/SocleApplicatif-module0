"""Tests unitaires pour les composants ML et NLP."""

from pathlib import Path

from backend.main import DOCUMENT_LABELS
from iatos_core.ml.document import DocumentAnalyzer
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


def test_document_analyzer():
    analyzerDoc = DocumentAnalyzer()
    
    # Cas passeport
    image_bytes1 = Path(".\\tests\\fichiersTests\\AnalyseDocuments\\passeport\\passport1.jpg").read_bytes()
    results1 = analyzerDoc.classify(image_bytes1, DOCUMENT_LABELS)
    detected_document1=results1[0]["label"]
    confidence1=results1[0]["score"]
    assert detected_document1 == "la photo d'un passeport"
    assert confidence1 >= 0.9

    # Cas relevé de compte
    image_bytes2 = Path(".\\tests\\fichiersTests\\AnalyseDocuments\\releve_compte\\bank1.jpg").read_bytes()
    results2 = analyzerDoc.classify(image_bytes2, DOCUMENT_LABELS)
    detected_document2=results2[0]["label"]
    confidence2=results2[0]["score"]
    #assert detected_document2 == "la photo d'un relevé de compte"
    #assert confidence2 >= 0.9
    
    # Cas chèque
    image_bytes3 = Path(".\\tests\\fichiersTests\\AnalyseDocuments\\cheque\\cheque2.jpg").read_bytes()
    results3 = analyzerDoc.classify(image_bytes3, DOCUMENT_LABELS)
    detected_document3=results3[0]["label"]
    confidence3=results3[0]["score"]
    #assert detected_document3 == "la photo d'un chèque"
    #assert confidence3 >= 0.9
          
    # Cas page blanche
    image_bytes4 = Path(".\\tests\\fichiersTests\\AnalyseDocuments\\pageBlanche\\PageBlanche.png").read_bytes()
    results4 = analyzerDoc.classify(image_bytes4, DOCUMENT_LABELS)
    detected_document4=results4[0]["label"]
    confidence4=results4[0]["score"]
    assert detected_document4 == "la photo d'une page blanche"
    assert confidence4 >= 0.5  