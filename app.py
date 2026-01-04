from flask import Flask, render_template, request, redirect
from recommender import MovieRecommender
from data_loader import load_from_bigquery
import pandas as pd

app = Flask(__name__)

# --- INITIALISATION ---
# On charge les vraies données au démarrage
df_movies, df_ratings = load_from_bigquery()

# On initialise l'IA
rec_sys = MovieRecommender()
rec_sys.load_data(df_ratings, df_movies)
rec_sys.train()

@app.route('/')
def index():
    # Augmentons à 1000 ou supprimons .head() pour tout avoir
    # Attention : charger 10 000 films peut ralentir le menu déroulant du navigateur
    movie_list = df_movies.head(1000).to_dict('records') 
    return render_template('index.html', movies=movie_list)

@app.route('/recommend')
def recommend():
    user_id = int(request.args.get('user_id', 1))
    recs = rec_sys.get_recommendations_for_user(user_id)
    
    # On remet aussi 1000 ici pour garder la cohérence après le calcul
    movie_list = df_movies.head(1000).to_dict('records')
    return render_template('index.html', 
                           tables=recs.to_html(classes='data', index=False), 
                           user_id=user_id, 
                           movies=movie_list)

@app.route('/add_rating')
def add_rating():
    global df_ratings
    try:
        # On récupère l'ID choisi dans le formulaire
        user_id = int(request.args.get('user_id'))
        m_id = int(request.args.get('movie_id'))
        rate = float(request.args.get('rating'))
        
        # Mise à jour des données
        new_data = pd.DataFrame([{'userId': user_id, 'movieId': m_id, 'rating': rate}])
        df_ratings = rec_sys.add_new_user_ratings(new_data, df_ratings)
        
        return f"""
        <html>
            <body style="font-family: sans-serif; text-align: center; padding-top: 50px;">
                <h2 style="color: green;">✅ Note enregistrée pour l'utilisateur {user_id} !</h2>
                <p>Le film {m_id} a reçu la note de {rate}/5.</p>
                <a href="./recommend?user_id={user_id}" style="text-decoration: none; background: #1a73e8; color: white; padding: 10px 20px; border-radius: 5px;">
                    Voir les recommandations mises à jour
                </a>
            </body>
        </html>
        """
    except Exception as e:
        return f"Erreur : {str(e)}"
if __name__ == '__main__':
    # On lance sur le port 8081 car 8080 est souvent occupé
    app.run(host='0.0.0.0', port=8081)