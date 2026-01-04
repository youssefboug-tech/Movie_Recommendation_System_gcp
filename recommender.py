import pandas as pd
from surprise import SVD, Dataset, Reader

class MovieRecommender:
    def __init__(self):
        # Paramètres optimisés pour un bon compromis RMSE/Performance
        self.algo = SVD(n_factors=100, n_epochs=20, lr_all=0.005, reg_all=0.1)
        self.data = None
        self.trainset = None
        self.movies_df = None
    
    def load_data(self, df_ratings, df_movies):
        """Prépare les données pour l'algorithme."""
        self.movies_df = df_movies
        reader = Reader(rating_scale=(0.5, 5.0))
        # Surprise a besoin des colonnes : userId, movieId, rating
        self.data = Dataset.load_from_df(df_ratings[['userId', 'movieId', 'rating']], reader)

    def train(self):
        """Entraîne le modèle sur toutes les données chargées."""
        self.trainset = self.data.build_full_trainset()
        self.algo.fit(self.trainset)

    def get_recommendations_for_user(self, user_id, top_n=10):
        """Génère des recommandations hybrides (SVD + Boost de genre)."""
        try:
            # Récupérer l'ID interne de l'utilisateur
            u_inner_id = self.trainset.to_inner_uid(user_id)
            user_ratings = self.trainset.ur[u_inner_id]
            
            # Identifier ses genres préférés (films notés >= 4)
            fav_genres = []
            for m_iid, r in user_ratings:
                if r >= 4.0:
                    m_id = self.trainset.to_raw_iid(m_iid)
                    genre_str = self.movies_df[self.movies_df['movieId'] == m_id]['genres'].values[0]
                    fav_genres.extend(genre_str.split('|'))
            
            seen_ids = [self.trainset.to_raw_iid(iid) for (iid, _) in user_ratings]
        except ValueError:
            # Utilisateur inconnu (nouveau)
            fav_genres = []
            seen_ids = []

        # --- LOGIQUE STRICTE POUR DES RÉSULTATS ADÉQUATS ---
        all_ids = self.movies_df['movieId'].unique()
        preds = []
        
        for m_id in all_ids:
            if m_id not in seen_ids:
                # 1. Analyse des genres du film
                movie_genres = self.movies_df[self.movies_df['movieId'] == m_id]['genres'].values[0].split('|')
                common = set(fav_genres).intersection(set(movie_genres))
                
                # 2. FILTRAGE STRICT : 
                # Si l'utilisateur a des préférences mais que le film n'en fait pas partie, on l'ignore
                if fav_genres and not common:
                    continue 
                
                # 3. SCORE IA :
                # On utilise le SVD pour classer uniquement les films qui ont passé le filtre
                pred_score = self.algo.predict(user_id, m_id).est
                
                # Petit bonus pour les films qui cochent PLUSIEURS de vos genres préférés
                final_score = pred_score + (len(common) * 0.5)
                
                preds.append((m_id, min(final_score, 5.0)))

        # 4. Tri final
        preds.sort(key=lambda x: x[1], reverse=True)
        
        final_list = []
        for m_id, score in preds[:top_n]:
            info = self.movies_df[self.movies_df['movieId'] == m_id].iloc[0]
            final_list.append({
                'movieId': m_id, 
                'title': info['title'], 
                'genres': info['genres'], 
                'score': round(score, 2)
            })
        return pd.DataFrame(final_list)

    def add_new_user_ratings(self, new_ratings_df, df_ratings_original):
        """Ajoute des notes et ré-entraîne le modèle immédiatement."""
        updated_df = pd.concat([df_ratings_original, new_ratings_df], ignore_index=True)
        self.load_data(updated_df, self.movies_df)
        self.train()
        return updated_df