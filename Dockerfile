FROM python:3.9-slim

# les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    git \
    libpq-dev \
    gcc \
    && apt-get clean

WORKDIR /app

COPY . /app

# PYTHONPATH pour import les modules python 
ENV PYTHONPATH="/app/src"

# ca installe toutes les dependances du project
RUN pip install --no-cache-dir -r requirements.txt

# lance le main.py (notre jeux)
CMD ["python", "src/app/main.py"]
