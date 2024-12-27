# Utilise une image Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY requirements.txt /app/
COPY src /app/src/

# Installer les dépendances via pip (à partir de requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut pour exécuter votre application
CMD ["python", "src/app/main.py"]

