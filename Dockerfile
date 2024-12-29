# Utiliser une image de base Python légère
FROM python:3.9-slim

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    git \
    libpq-dev \
    gcc \
    && apt-get clean

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY . /app

# Ajouter `src` au PYTHONPATH
ENV PYTHONPATH="/app/src"

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut pour exécuter l'application
CMD ["python", "src/app/main.py"]
