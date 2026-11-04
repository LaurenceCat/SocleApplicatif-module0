# 1. Image de base légère et sécurisée
FROM python:3.11-slim

# 2. Variables d'environnement Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Répertoire de travail
WORKDIR /app

# 4. Installation de uv pour un build ultra-rapide
RUN pip install --no-cache-dir uv

# 5. Optimisation du cache Docker : copier pyproject.toml et README d'abord !
COPY pyproject.toml README.md ./
COPY src ./src

# 6. Installation des dépendances via uv dans le Python système
RUN uv pip install --no-cache --system -e .

# 7. Copier le reste du code source
COPY . .

# 8. Exposition du port API
EXPOSE 8000

# 9. Commande de lancement uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
