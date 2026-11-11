"""Schemas Pydantic pour l'API FastAPI."""

from typing import Dict, List, Optional
from pydantic import BaseModel, Field


# Schemas pour le Chatbot LangGraph
class ChatMessage(BaseModel):
    role: str = Field(..., description="Role de l'emetteur : 'user' ou 'assistant'")
    content: str = Field(..., description="Contenu texte du message")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Message saisi par l'utilisateur")
    history: List[ChatMessage] = Field(default_factory=list, description="Historique de la conversation")


class ChatResponse(BaseModel):
    success: bool
    response: str
    tool_called: bool
    tool_results: List[str] = Field(default_factory=list)


# Schemas pour la Prediction de Credit
class CreditPredictRequest(BaseModel):
    montant_demande: float = Field(..., gt=0, le=500000, description="Montant souhaite en euros")
    duree_mois: int = Field(..., ge=6, le=360, description="Duree du pret en mois")
    revenu_mensuel: float = Field(..., gt=0, le=100000, description="Revenu mensuel net en euros")


class CreditPredictResponse(BaseModel):
    score: float
    decision: str
    motif: str
    features_utilisees: Dict[str, float]
    type_modele: str


# Schemas pour l'Analyse de Sentiment
class SentimentPredictRequest(BaseModel):
    texte: str = Field(..., min_length=1, description="Texte de l'avis ou du message a analyser")


class SentimentPredictResponse(BaseModel):
    texte: str
    compound: float
    label: str
    scores: Dict[str, float]
    type_modele: str


# Schema de statut de service
class HealthResponse(BaseModel):
    status: str
    version: str
    service: str



# Schemas pour l'Analyse de Documents

# class DocumentPredictRequest(BaseModel):
#    texte: str = Field(..., min_length=1, description="Document a analyser")
# -> inutile dans le cas de l'analyse de document

# Réponse JSON attendue sur l'API (POST /vision/classify-document):    
class DocumentClassScore(BaseModel):
    label: str
    score: float

class DocumentClassificationResponse(BaseModel):
    filename: str
    detected_document: str
    confidence: float
    candidates: List[DocumentClassScore]