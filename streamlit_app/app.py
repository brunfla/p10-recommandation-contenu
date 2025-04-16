import streamlit as st
import requests
import pandas as pd
import os

# --- LOGGING (stdout pour Docker logs) ---
import logging
import sys
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

# Lire la variable d’environnement "LOCAL"
LOCAL = os.environ.get("LOCAL", "false").lower() == "true"

# Définir l'URL de base selon l'environnement
if LOCAL:
    BASE_URL = "http://azure_function:7071/api"
    logger.info("🌍 Mode LOCAL activé")
else:
    BASE_URL = "https://p10.azurewebsites.net/api"
    logger.info("☁️ Mode PRODUCTION activé")

# Endpoints des API
COLLAB_ENDPOINT = f"{BASE_URL}/recommend-articles-collaborative"
CONTENT_ENDPOINT = f"{BASE_URL}/recommend-articles-content"

# --- Interface Streamlit ---
st.set_page_config(page_title="Système de Recommandation", layout="centered")

st.title("🎯 Système de Recommandation d’Articles")
st.markdown("Testez les deux moteurs : *Collaboratif* et *Content-Based Filtering*")

# --- Sélection de l'utilisateur ---
user_ids = [501, 502, 503, 504, 505]
selected_user = st.selectbox("Sélectionnez un utilisateur", user_ids)
logger.info(f"👤 Utilisateur sélectionné : {selected_user}")

# --- Choix du moteur de recommandation ---
mode = st.radio("Choisissez le moteur de recommandation :", ["Collaboratif", "Content-Based"])
logger.info(f"⚙️ Moteur sélectionné : {mode}")

# --- Charger les clics depuis un fichier CSV ---
@st.cache_data
def load_clicks(csv_path="clicks.csv"):
    df = pd.read_csv(csv_path)
    logger.info(f"📂 Clics chargés depuis {csv_path} ({len(df)} lignes)")
    return df

clicks_df = load_clicks()

# Préparer le dernier clic uniquement pour le content-based
user_clicks_df = clicks_df[clicks_df["user_id"] == selected_user]
user_clicks_df = user_clicks_df.sort_values(by="click_timestamp", ascending=False)

# Par défaut, pas de clic à envoyer
real_clicks = []

if not user_clicks_df.empty:
    last_click = user_clicks_df.iloc[0]
    real_clicks = [{
        "user_id": selected_user,
        "click_article_id": int(last_click["click_article_id"]),
        "click_timestamp": int(last_click["click_timestamp"])
    }]
    logger.info(f"🖱️ Dernier clic utilisé : {real_clicks[0]}")
else:
    logger.warning("⚠️ Aucun clic trouvé pour cet utilisateur.")

# --- Lancer la recommandation ---
if st.button("📡 Lancer la recommandation"):
    with st.spinner("Analyse en cours..."):
        try:
            if mode == "Collaboratif":
                payload = {"user_id": selected_user}
                url = COLLAB_ENDPOINT
            else:
                if not real_clicks:
                    st.warning("Aucun clic trouvé pour cet utilisateur.")
                    logger.warning("🚫 Recommandation annulée : pas de clic")
                    st.stop()

                payload = {
                    "user_id": selected_user,
                    "clicks": real_clicks  # Seulement le dernier clic
                }
                url = CONTENT_ENDPOINT

            logger.info(f"📤 Requête envoyée à {url}")
            logger.info(f"Payload : {payload}")

            response = requests.post(url, json=payload)
            logger.info(f"📥 Réponse reçue : {response.status_code}")

            if response.status_code == 200:
                result = response.json()
                articles = result.get("recommended_articles", [])
                logger.info(f"✅ Articles recommandés : {articles}")
                if articles:
                    st.success("✅ Recommandations générées !")
                    st.markdown("**Articles recommandés :**")
                    st.write(articles)
                else:
                    st.warning("Aucune recommandation trouvée pour cet utilisateur.")
                    logger.warning("⚠️ Liste d’articles vide")
            else:
                st.error(f"❌ Erreur {response.status_code} : {response.text}")
                logger.error(f"❌ Erreur API : {response.status_code} - {response.text}")

        except Exception as e:
            st.exception(f"Erreur lors de la requête : {str(e)}")
            logger.exception("❌ Exception pendant l'appel API")
