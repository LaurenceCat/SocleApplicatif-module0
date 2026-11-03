"""Tests d'integration pour les routes FastAPI."""

from unittest.mock import patch


def test_endpoint_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "iatos-api"
    assert "version" in data


def test_endpoint_predict_credit_success(client):
    payload = {
        "montant_demande": 10000.0,
        "duree_mois": 24,
        "revenu_mensuel": 3500.0,
    }
    response = client.post("/predict/credit", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "score" in data
    assert 300.0 <= data["score"] <= 850.0
    assert data["decision"] in ["Favorable", "Ajourne / Examen Approfondi", "Defavorable"]


def test_endpoint_predict_credit_validation_error(client):
    # Montant negatif interdit par Pydantic gt=0
    payload = {
        "montant_demande": -500.0,
        "duree_mois": 24,
        "revenu_mensuel": 3500.0,
    }
    response = client.post("/predict/credit", json=payload)
    assert response.status_code == 422


def test_endpoint_predict_sentiment_success(client):
    payload = {"texte": "Outstanding technical performance and great developer experience."}
    response = client.post("/predict/sentiment", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "Positif"
    assert data["compound"] > 0


def test_endpoint_chat_with_mocked_agent(client):
    # Mock de run_agent_message pour garantir l'execution sans dependance a Ollama en CI
    mock_result = {
        "success": True,
        "response": "Le resultat du calcul de 12 + 8 est 20.",
        "tool_called": True,
        "tool_results": ["Le resultat de 12.0 + 8.0 est 20.0"],
    }
    with patch("backend.main.run_agent_message", return_value=mock_result):
        payload = {
            "message": "Combien font 12 + 8 ?",
            "history": [],
        }
        response = client.post("/chat", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["tool_called"] is True
        assert "20" in data["response"]
