import streamlit as st
import requests
import pandas as pd
import os

# Lire la variable d’environnement "LOCAL"
LOCAL = os.environ.get("LOCAL", "true").lower() == "false"

if LOCAL:
    BASE_URL = "http://localhost:7072/api"
else:
    BASE_URL = "https://p10.azurewebsites.net/api"

COLLAB_ENDPOINT = f"{BASE_URL}/recommend-articles-collaborative"
CONTENT_ENDPOINT = f"{BASE_URL}/recommend-articles-content"

# --- Interface Streamlit ---
st.set_page_config(page_title="Système de Recommandation", layout="centered")

st.title("🎯 Système de Recommandation d’Articles")
st.markdown("Testez les deux moteurs : *Collaboratif* et *Content-Based Filtering*")

# --- Simuler des user_id (ou charger un fichier) ---
# Exemple statique pour MVP
user_ids = [1001, 1002, 1003, 1004, 1005]
selected_user = st.selectbox("Sélectionnez un utilisateur", user_ids)

# --- Choix du moteur de reco ---
mode = st.radio("Choisissez le moteur de recommandation :", ["Collaboratif", "Content-Based"])

# --- Simuler des clics (pour content-based uniquement) ---
simulated_clicks = [
    {"user_id": selected_user, "click_article_id": 101, "click_timestamp": 1710001000},
    {"user_id": selected_user, "click_article_id": 202, "click_timestamp": 1710002000},
    {"user_id": selected_user, "click_article_id": 303, "click_timestamp": 1710003000},
]

if st.button("📡 Lancer la recommandation"):
    with st.spinner("Analyse en cours..."):
        try:
            if mode == "Collaboratif":
                payload = {"user_id": selected_user}
                url = COLLAB_ENDPOINT
            else:
                payload = {
                    "user_id": selected_user,
                    "clicks": simulated_clicks
                }
                url = CONTENT_ENDPOINT

            response = requests.post(url, json=payload)

            if response.status_code == 200:
                result = response.json()
                articles = result.get("recommended_articles", [])
                if articles:
                    st.success("✅ Recommandations générées !")
                    st.markdown("**Articles recommandés :**")
                    st.write(articles)
                else:
                    st.warning("Aucune recommandation trouvée pour cet utilisateur.")
            else:
                st.error(f"❌ Erreur {response.status_code} : {response.text}")

        except Exception as e:
            st.exception(f"Erreur lors de la requête : {str(e)}")

