from google.cloud import bigquery
import pandas as pd

def load_from_bigquery():
    MY_PROJECT_ID = "students-group3" 
    # Initialisation du client BigQuery
    client = bigquery.Client(project=MY_PROJECT_ID)

    
    # 1. Chargement des Films (Movies)
    # On récupère l'ID, le titre et les genres.
    query_movies = """
    SELECT 
        movieId,
        title,
        genres
    FROM 
        `master-ai-cloud.MoviePlatform.movies`
    """
    df_movies = client.query(query_movies).to_dataframe()

    # 2. Chargement des Notes (Ratings)
    # On limite pour l'instant pour tester, mais pour le modèle final on prendra tout.
    # Le document conseille d'utiliser LIMIT pour l'exploration[cite: 34].
    # Ici, je mets une limite pour l'EDA rapide, on l'enlèvera pour l'entraînement.
    query_ratings = """
        SELECT 
        userId,
        movieId,
        rating,
        timestamp
    FROM 
        `master-ai-cloud.MoviePlatform.ratings`
    LIMIT 100000  
    """
    # Note: J'ai mis 100k lignes pour avoir assez de stats sans tout charger si la table est géante.
    df_ratings = client.query(query_ratings).to_dataframe()

    print(f"Films chargés : {df_movies.shape}")
    print(f"Notes chargées : {df_ratings.shape}")
    
    return df_movies, df_ratings