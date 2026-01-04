# 🎬 Système de Recommandation de Films - Architecture Hybride sur GCP

**Projet Master AI & Cloud** *Ce projet implémente une architecture complète de Machine Learning, de l'extraction de données BigQuery jusqu'à une interface utilisateur conteneurisée.*

---

## 🚀 Fonctionnalités Clés

1.  **Modèle Hybride Avancé** : Combinaison de **SVD (Collaborative Filtering)** et de **Filtrage basé sur le contenu (Content-Based)**.
    * *Pourquoi ?* Le SVD assure la précision globale (RMSE optimisé), tandis que le boost de contenu résout le problème du **"Cold Start"** (démarrage à froid) pour les nouveaux utilisateurs.
2.  **Entraînement en Temps Réel** : Le modèle se met à jour instantanément lorsqu'un utilisateur ajoute une note.
3.  **Architecture Cloud Native** : Application développée en Python/Flask et entièrement conteneurisée avec Docker.
4.  **Données Réelles** : Connexion directe au dataset `MoviePlatform` sur Google BigQuery.

---

## 🛠️ Stack Technique

* **Langage** : Python 3.9
* **Interface Web** : Flask & Jinja2
* **ML Engine** : Scikit-Surprise (SVD) + Pandas (Logique Hybride)
* **Database** : Google Cloud BigQuery
* **Containerisation** : Docker
* **Serveur de Prod** : Gunicorn

---

## ⚙️ Installation et Lancement (Local & Docker)

Le projet est conçu pour être lancé via Docker pour garantir l'isolation des dépendances.

### 1. Pré-requis
* Avoir Docker installé.
* Avoir accès aux crédentiels Google Cloud (pour BigQuery).

### 2. Construction de l'image
À la racine du projet :
```bash
docker build -t movie-app .