# 1. Image de base légère avec Python 3.9
FROM python:3.9-slim

# 2. Définir le répertoire de travail dans le container
WORKDIR /app

# 3. Installer les dépendances système (nécessaires pour compiler scikit-surprise)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 4. Copier et installer les bibliothèques Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier tout votre code (app.py, recommender.py, data_loader.py et templates/)
COPY . .

# 6. Exposer le port que nous utilisons (8081)
EXPOSE 8081

# 7. Lancer l'application avec Gunicorn (serveur de production)
CMD ["gunicorn", "--bind", "0.0.0.0:8081", "--timeout", "120", "app:app"]