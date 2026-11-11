"""Module de scoring de credit utilisant la regression lineaire baseline."""

from pathlib import Path
from typing import Dict, Any
import joblib
import pandas as pd
from iatos_core.config import CLIP_MODEL_PATH, CLIP_DEVICE
from iatos_core.logger import logger
import io
from pathlib import Path

import torch
from PIL import Image
from transformers import CLIPModel, CLIPProcessor



class DocumentAnalyzer:
    """Encapsule CLIP pour classer des images/documents en zero-shot."""

    def __init__(self, model_path: Path = CLIP_MODEL_PATH, device: str = CLIP_DEVICE):
        self.model_path = Path(model_path)
        self.device = device
        self._model = None
        self._processor = None
        self._load_model()

    def _load_model(self) -> None:
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Modèle introuvable : {self.model_path}. "
                "Lancez : hf download openai/clip-vit-base-patch32 --local-dir ..."
            )
        self._processor = CLIPProcessor.from_pretrained(self.model_path)
        self._model = CLIPModel.from_pretrained(self.model_path).to(self.device)
        self._model.eval()

    @staticmethod
    def _to_image(data: bytes | Image.Image) -> Image.Image:
        if isinstance(data, bytes):
            data = Image.open(io.BytesIO(data))
        return data.convert("RGB")

    @torch.no_grad()
    def classify(self, image: bytes | Image.Image, labels: list[str]) -> list[dict]:
        """Classe l'image parmi les libellés donnés (zero-shot)."""
        inputs = self._processor(
            text=labels, images=self._to_image(image),
            return_tensors="pt", padding=True,
        ).to(self.device)
        probs = self._model(**inputs).logits_per_image.softmax(dim=1)[0]
        results = [{"label": l, "score": float(p)} for l, p in zip(labels, probs)]
        return sorted(results, key=lambda r: r["score"], reverse=True)

    @torch.no_grad()
    def embed_image(self, image: bytes | Image.Image) -> list[float]:
        """Retourne l'embedding de l'image (utile pour la recherche par similarité)."""
        inputs = self._processor(images=self._to_image(image), return_tensors="pt").to(self.device)
        return self._model.get_image_features(**inputs)[0].tolist()