"""Configuration centrale pour iatos_core."""

import os
from pathlib import Path

# Chemins principaux du projet
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# S'assurer que les répertoires nécessaires existent
MODELS_DIR.mkdir(parents=True, exist_ok=True)
LOGS_DIR.mkdir(parents=True, exist_ok=True)

# Configuration Ollama et Agent LangGraph
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
OLLAMA_TEMPERATURE = float(os.getenv("OLLAMA_TEMPERATURE", "0.0"))

# Chemins des modèles sérialisés
CREDIT_MODEL_PATH = MODELS_DIR / "credit_linear_model.joblib"
DATASET_PATH = DATA_DIR / "credit_risk_dataset.csv"

# Configuration du modèle pour les documents
CLIP_MODEL_PATH = Path(os.getenv("CLIP_MODEL_PATH", "models/clip-vit-base-patch32"))
CLIP_DEVICE = os.getenv("CLIP_DEVICE", "cpu")  # "cuda" si GPU

# Configuration API
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
FASTAPI_BACKEND_URL = os.getenv("FASTAPI_BACKEND_URL", "http://localhost:8000")
