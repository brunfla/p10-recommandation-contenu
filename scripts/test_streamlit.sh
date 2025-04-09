#!/bin/bash

if [ "$GH_CI" = "true" ]; then
  echo "🚀 [CI] Streamlit test – à définir selon le pipeline CI"

  echo "📡 Envoi de la requête à Azure Function (collaborative)..."
  RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST https://p10.azurewebsites.net/api/recommend-articles-collaborative \
    -H "Content-Type: application/json" \
    -d '{"user_id": 123}')

  echo "$RESPONSE" | tee .dvc/tmp/test_output.txt

  HTTP_CODE=$(echo "$RESPONSE" | grep HTTP_CODE | cut -d':' -f2)

  # 👇 Initialiser un flag pour savoir si on a une erreur
  ERROR_OCCURRED=false

  if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Requête réussie (200)"
  else
    echo "❌ Échec de la requête (HTTP $HTTP_CODE)"
    ERROR_OCCURRED=true
  fi
else
  echo "🧪 [LOCAL] Lancement des tests Streamlit + Azure Functions..."

  echo "⏳ Attente du démarrage complet des services..."
  sleep 5

  echo "📡 Envoi de la requête à Azure Function (collaborative)..."
  RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://localhost:7072/api/recommend-articles-collaborative \
    -H "Content-Type: application/json" \
    -d '{"user_id": 123}')

  echo "$RESPONSE" | tee .dvc/tmp/test_output.txt

  HTTP_CODE=$(echo "$RESPONSE" | grep HTTP_CODE | cut -d':' -f2)

  # 👇 Initialiser un flag pour savoir si on a une erreur
  ERROR_OCCURRED=false

  if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Requête réussie (200)"
  else
    echo "❌ Échec de la requête (HTTP $HTTP_CODE)"
    ERROR_OCCURRED=true
  fi

  echo "🛑 Arrêt des services en fond..."
  FUNC_PID=$(pgrep func)
  echo "🔪 kill Azure Function (PID $FUNC_PID)"
  kill -9 "$FUNC_PID" || echo "⚠️ Impossible de kill le process $FUNC_PID"

  # Optionnel : Streamlit si tu le démarres
  # if [ -f .dvc/tmp/streamlit.pid ]; then
  #   STREAMLIT_PID=$(cat .dvc/tmp/streamlit.pid)
  #   echo "🔪 kill Streamlit (PID $STREAMLIT_PID)"
  #   kill "$STREAMLIT_PID" || echo "⚠️ Impossible de kill le process $STREAMLIT_PID"
  # fi

  # 👇 On quitte avec le bon code à la fin
  if [ "$ERROR_OCCURRED" = true ]; then
    exit 1
  fi
fi
