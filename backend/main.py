"""Point d'entree principal de l'API FastAPI - Starter Kit Apprenants.

Ce fichier est le coeur de votre mission pour le backend de la plateforme IA-TOS.
Vous devez completer les routes ci-dessous en vous appuyant sur :
- Le package metier : iatos_core (agents, scoring, sentiment, logger, config)
- Le contrat d'interface : backend.schemas (Pydantic v2)
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from iatos_core import __version__
from iatos_core.logger import logger
from iatos_core.ml.scoring import CreditScoringPredictor
from iatos_core.ml.sentiment import SentimentAnalyzer
from iatos_core.agent.graph import run_agent_message

from backend.schemas import (
    ChatRequest,
    ChatResponse,
    CreditPredictRequest,
    CreditPredictResponse,
    HealthResponse,
    SentimentPredictRequest,
    SentimentPredictResponse,
)

# Services partages (Singletons en memoire)
scoring_predictor: CreditScoringPredictor = None
sentiment_analyzer: SentimentAnalyzer = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cycle de vie de l'application FastAPI.
    
    TODO (Apprenants) :
    1. Instancier le CreditScoringPredictor() et l'assigner a la variable globale scoring_predictor.
    2. Instancier le SentimentAnalyzer() et l'assigner a la variable globale sentiment_analyzer.
    3. Logger le succes de l'initialisation avec loguru.
    """
    
    global scoring_predictor, sentiment_analyzer
    logger.info("Demarrage des services FastAPI IA-TOS...")
    
    #1.
    scoring_predictor = CreditScoringPredictor()
    
    #2.
    sentiment_analyzer = SentimentAnalyzer()
    
    #3.
    logger.success("Modeles initialises : CreditScoringPredictor et SentimentAnalyzer.")
    
    # TODO: Initialisez vos modeles ici
    
    scoring_predictor = CreditScoringPredictor()
    sentiment_analyzer = SentimentAnalyzer()
    
    yield
    logger.info("Arret des services FastAPI IA-TOS.")


# Instanciation de l'application FastAPI
app = FastAPI(
    title="Plateforme IA-TOS - API Multi-Services",
    description="API exposant l'agent conversationnel LangGraph, le scoring de credit et l'analyse de sentiment.",
    version=__version__,
    lifespan=lifespan,
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["Supervision"])
def health_check():
    """Endpoint de surveillance (Healthcheck) pour Uptime Kuma ou Docker.
    
    TODO (Apprenants) :
    Retourner une instance de HealthResponse avec :
    - status="ok"
    - version=__version__
    - service="iatos-api"
    """
    
    return HealthResponse(
        status="ok",
        version=__version__,
        service="iatos-api",
    )
    
    # TODO: Remplacer par votre implementation
    #raise HTTPException(
    #    status_code=501, 
    #   detail="Endpoint /health non implemente. A vous de jouer !"
    #)


@app.post("/chat", response_model=ChatResponse, tags=["Agent Conversationnel"])
def chat_endpoint(payload: ChatRequest):
    """Endpoint conversationnel interrogeant l'agent LangGraph outille.
    
    TODO (Apprenants) :
    1. Convertir l'historique Pydantic (payload.history) en liste de dictionnaires [{'role': ..., 'content': ...}].
    2. Appeler run_agent_message(user_message=payload.message, history=history_dicts).
    3. Retourner une instance de ChatResponse avec :
       - success (bool)
       - response (str)
       - tool_called (bool)
       - tool_results (list[str])
    4. Gerer les exceptions potentielles avec un logger.error et un HTTPException(500).
    """
    
    try:
        # 1. Historique Pydantic -> liste de dictionnaires
        history_dicts = [
            {"role": msg.role, "content": msg.content}
            for msg in payload.history
        ]

        # 2. Appel de l'agent
        result = run_agent_message(
            user_message=payload.message,
            history=history_dicts,
        )

        # 3. Construction de la reponse
        return ChatResponse(
            success=result.get("success", True),
            response=result.get("response", ""),
            tool_called=result.get("tool_called", False),
            tool_results=result.get("tool_results", []),
        )

    except Exception as e:
        # 4. Log + erreur HTTP 500
        logger.error(f"Erreur dans /chat : {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur interne lors de l'appel a l'agent.",
        )
    
    # TODO: Remplacer par votre implementation
    #raise HTTPException(
    #    status_code=501, 
    #    detail="Endpoint /chat non implemente. A vous de jouer !"
    #)


@app.post("/predict/credit", response_model=CreditPredictResponse, tags=["Scoring Tabulaire"])
def predict_credit(payload: CreditPredictRequest):
    """Endpoint de prediction du score de credit (baseline Scikit-Learn M0).
    
    TODO (Apprenants) :
    1. Recuperer l'instance globale de scoring_predictor (ou l'instancier si None).
    2. Appeler scoring_predictor.predict(...) avec montant_demande, duree_mois et revenu_mensuel.
    3. Retourner une instance de CreditPredictResponse avec les resultats.
    4. Gerer les exceptions potentielles avec un HTTPException(500).
    """
    
    global scoring_predictor
    try:
        #1. Recuperer l'instance globale
        if scoring_predictor is None:
            scoring_predictor = CreditScoringPredictor()

        #2. Prediction
        result = scoring_predictor.predict(
            montant_demande=payload.montant_demande,
            duree_mois=payload.duree_mois,
            revenu_mensuel=payload.revenu_mensuel,
        )

        #3. Construction de la reponse
        return CreditPredictResponse(**result)

    except Exception as e:
        #4.Log + erreur HTTP 500
        logger.error(f"Erreur dans /predict/credit : {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur interne lors de la prediction du score de credit.",
        )
    
    # TODO: Remplacer par votre implementation
    #raise HTTPException(
    #    status_code=501, 
    #    detail="Endpoint /predict/credit non implemente. A vous de jouer !"
    #)


@app.post("/predict/sentiment", response_model=SentimentPredictResponse, tags=["Traitement NLP"])
def predict_sentiment(payload: SentimentPredictRequest):
    """Endpoint d'analyse de polarite de sentiment (baseline NLTK VADER M0).
    
    TODO (Apprenants) :
    1. Recuperer l'instance globale de sentiment_analyzer (ou l'instancier si None).
    2. Appeler sentiment_analyzer.analyze(payload.texte).
    3. Retourner une instance de SentimentPredictResponse avec les resultats.
    4. Gerer les exceptions potentielles avec un HTTPException(500).
    """
    
    global sentiment_analyzer
    try:
        #1. Recuperer l'instance globale (ou l'instancier si None)
        if sentiment_analyzer is None:
            sentiment_analyzer = SentimentAnalyzer()

        #2. Analyse du texte
        result = sentiment_analyzer.analyze(payload.texte)

        #3. Construction de la reponse
        return SentimentPredictResponse(**result)

    except Exception as e:
        #4. Log + erreur HTTP 500
        logger.error(f"Erreur dans /predict/sentiment : {e}")
        raise HTTPException(
            status_code=500,
            detail="Erreur interne lors de l'analyse de sentiment.",
        )
    
    # TODO: Remplacer par votre implementation
    #raise HTTPException(
    #    status_code=501, 
    #   detail="Endpoint /predict/sentiment non implemente. A vous de jouer !"
    #)
