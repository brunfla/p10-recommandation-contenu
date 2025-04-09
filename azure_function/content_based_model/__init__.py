import azure.functions as func
import logging
import json
import pickle
import requests
import os
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# 📍 Lire l'environnement : "local" ou "production"
ENV = os.environ.get("ENVIRONMENT", "local").lower()

def load_embeddings():
    if ENV == "production":
        logging.info("📦 Chargement des embeddings depuis Azure Blob Storage (prod)")
        url = os.environ.get("CONTENT_MODEL_SAS_URL")
        response = requests.get(url)
        response.raise_for_status()
        return pickle.loads(response.content)
    else:
        logging.info("📦 Chargement des embeddings depuis un fichier local (dev)")
        local_path = os.path.join(os.path.dirname(__file__), "shared", "content_based_model.pkl")
        with open(local_path, "rb") as f:
            return pickle.load(f)

# ⏳ Chargement une seule fois au démarrage
try:
    df_embed = load_embeddings()["embeddings"]
    if df_embed is None or df_embed.empty:
        raise ValueError("Embeddings vides ou non chargés.")
except Exception as e:
    logging.exception("❌ Échec du chargement des embeddings content-based.")
    df_embed = None

# 🎯 Fonction content-based filtering
def recommend_content_based(user_id, clicks_df, embeddings_df, top_k=5):
    user_clicks = clicks_df[clicks_df["user_id"] == user_id]
    if user_clicks.empty:
        return []
    last_click = user_clicks.sort_values(by="click_timestamp", ascending=False).iloc[0]
    last_article_id = last_click["click_article_id"]

    article_embedding = embeddings_df[embeddings_df["article_id"] == last_article_id]
    if article_embedding.empty:
        return []

    base_vector = article_embedding.drop(columns=["article_id"]).values
    all_embeddings = embeddings_df.drop(columns=["article_id"]).values
    all_article_ids = embeddings_df["article_id"].values

    already_clicked_ids = user_clicks["click_article_id"].unique()
    similarities = cosine_similarity(base_vector, all_embeddings)[0]
    candidates = [(aid, score) for aid, score in zip(all_article_ids, similarities) if aid not in already_clicked_ids]
    top_articles = sorted(candidates, key=lambda x: x[1], reverse=True)[:top_k]
    return [int(article_id) for article_id, _ in top_articles]

# 🚀 Point d’entrée Azure Function (modèle V1)
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        if df_embed is None:
            return func.HttpResponse(
                "❌ Erreur serveur : embeddings non disponibles.",
                status_code=500
            )

        req_body = req.get_json()
        if req_body is None or "user_id" not in req_body or "clicks" not in req_body:
            return func.HttpResponse(
                "❌ Requête invalide : 'user_id' ou 'clicks' manquants.",
                status_code=400
            )

        user_id = int(req_body.get("user_id"))
        clicks_data = req_body.get("clicks")
        clicks_df = pd.DataFrame(clicks_data)

        recommendations = recommend_content_based(user_id, clicks_df, df_embed)
        return func.HttpResponse(
            json.dumps({"recommended_articles": recommendations}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.exception("Erreur dans main() - content based")
        return func.HttpResponse(
            f"Erreur interne dans main() : {str(e)}",
            status_code=500
        )
