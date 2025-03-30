import azure.functions as func
import logging
import json
import pickle
import requests
import os

from surprise import SVD  # pour que pickle fonctionne
from surprise.trainset import Trainset

app = func.FunctionApp()

MODEL_URL = os.environ.get("MODEL_SAS_URL")

# 📥 Charger modèle depuis Azure Blob Storage
def load_model_from_blob(url):
    response = requests.get(url)
    response.raise_for_status()
    return pickle.loads(response.content)

# ⏳ Charger une seule fois au démarrage de la Function App
model, trainset = load_model_from_blob(MODEL_URL)

# 🎯 Logique de recommandation
def get_top_5(user_id, model, trainset, n=5):
    all_article_ids = trainset._raw2inner_id_items.keys()
    read_articles = set([j for (j, _) in trainset.ur[trainset.to_inner_uid(user_id)]]) \
        if user_id in trainset._raw2inner_id_users else set()
    candidates = [aid for aid in all_article_ids if aid not in read_articles]
    predictions = [(aid, model.predict(user_id, aid).est) for aid in candidates]
    top_n = sorted(predictions, key=lambda x: x[1], reverse=True)[:n]
    return [int(article_id) for article_id, _ in top_n]

# 🚀 Fonction Azure exposée via HTTP POST
@app.route(route="RecommendArticles", auth_level=func.AuthLevel.ANONYMOUS)
def RecommendArticles(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        user_id = int(req_body.get("user_id"))
        recommendations = get_top_5(user_id, model, trainset)
        return func.HttpResponse(
            json.dumps({"recommended_articles": recommendations}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.exception("Erreur dans la fonction RecommendArticles")
        return func.HttpResponse(
            f"Erreur : {str(e)}",
            status_code=400
        )
