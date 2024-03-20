# Étape de construction pour installer les dépendances
FROM python:3.11 as builder

# Installation de spaCy et téléchargement des modèles linguistiques
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Étape finale pour exécuter l'application, en utilisant python:3.11-slim
FROM python:3.11-slim

# Copie des artefacts nécessaires depuis l'étape de construction
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Configuration du répertoire de travail
WORKDIR /var/task/

# Install le CURL avec nettoyage pour alléger l'image
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copie de la fonction Lambda et des fichiers nécessaires
COPY main.py main.py
COPY model.h5 model.h5

# Configuration du Healthcheck
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:80/healthcheck || exit 1

# Commande par défaut pour l'exécution de la fonction Lambda
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
