import azure.functions as func
import logging
import json
import pickle
import requests
import os

from surprise import SVD  # pour que pickle fonctionne
from surprise.trainset import Trainset

# 📍 Lire l’environnement : "local" ou "production"
ENV = os.environ.get("ENVIRONMENT", "local").lower()

def load_model():
    if ENV == "production":
        logging.info("📦 Chargement du modèle SVD depuis Azure Blob Storage")
        url = os.environ.get("MODEL_SAS_URL")
        response = requests.get(url)
        response.raise_for_status()
        return pickle.loads(response.content)
    else:
        logging.info("📦 Chargement du modèle SVD depuis un fichier local")
        local_path = os.path.join(
            os.path.dirname(__file__),
            "shared",
            "collaborative_filtering_svd.pkl"
        )
        with open(local_path, "rb") as f:
            return pickle.load(f)

# ⏳ Chargement une seule fois
try:
    model, trainset = load_model()
    if not model or not trainset:
        raise ValueError("Modèle ou trainset vide.")
except Exception as e:
    logging.exception("❌ Échec du chargement du modèle collaborative filtering.")
    model = None
    trainset = None

# 🎯 Logique de recommandation
def get_top_5(user_id, model, trainset, n=5):
    all_article_ids = trainset._raw2inner_id_items.keys()
    read_articles = set([j for (j, _) in trainset.ur[trainset.to_inner_uid(user_id)]]) \
        if user_id in trainset._raw2inner_id_users else set()
    candidates = [aid for aid in all_article_ids if aid not in read_articles]
    predictions = [(aid, model.predict(user_id, aid).est) for aid in candidates]
    top_n = sorted(predictions, key=lambda x: x[1], reverse=True)[:n]
    return [int(article_id) for article_id, _ in top_n]

# 🚀 Point d’entrée Azure Function (modèle V1)
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if model is None or trainset is None:
            return func.HttpResponse(
                "❌ Erreur serveur : modèle non disponible.",
                status_code=500
            )

        req_body = req.get_json()
        if req_body is None or "user_id" not in req_body:
            return func.HttpResponse(
                "❌ Requête invalide : 'user_id' manquant.",
                status_code=400
            )

        user_id = int(req_body.get("user_id"))
        recommendations = get_top_5(user_id, model, trainset)
        return func.HttpResponse(
            json.dumps({"recommended_articles": recommendations}),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        logging.exception("Erreur dans main()")
        return func.HttpResponse(
            f"Erreur interne dans main() : {str(e)}",
            status_code=500
        )

