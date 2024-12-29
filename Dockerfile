# Utiliser une image de base Python
FROM python:3.9-slim

# Installer Git
RUN apt-get update && apt-get install -y git && apt-get clean

# Définir le répertoire de travail
WORKDIR /app

# Copier tous les fichiers nécessaires dans le conteneur
COPY . /app

# Installer les dépendances et le package local
RUN pip install --no-cache-dir .

# Commande par défaut pour exécuter ton application
CMD ["python", "-m", "app"]
