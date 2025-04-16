#!/bin/bash
set -e

ERROR_OCCURRED=false

if [ "$GH_CI" = "true" ]; then
  echo "[CI] ⏳ Attente du démarrage complet des services..."
  sleep 120

  echo "[CI] 📡 Envoi de la requête à Azure Function (collaborative)..."
  RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST https://p10.azurewebsites.net/api/recommend-articles-collaborative \
    -H "Content-Type: application/json" \
    -d '{"user_id": 123}')
  echo "$RESPONSE" | tee .dvc/tmp/test_output_collaborative.txt

  HTTP_CODE=$(echo "$RESPONSE" | grep HTTP_CODE | cut -d':' -f2)
  if [ "$HTTP_CODE" = "200" ]; then
    echo "[CI] ✅ Requête collaborative réussie (200)"
  else
    echo "[CI] ❌ Échec de la requête collaborative (HTTP $HTTP_CODE)"
    ERROR_OCCURRED=true
  fi
else
  echo "[LOCAL] ⏳ Attente du démarrage complet des services..."
  sleep 120

  echo "[LOCAL] 🧪 Lancement des tests Azure Functions..."

  echo "[LOCAL] 📡 Envoi de la requête à Azure Function (collaborative)..."
  RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://localhost:7071/api/recommend-articles-collaborative \
    -H "Content-Type: application/json" \
    -d '{"user_id": 123}')
  HTTP_CODE=$(echo "$RESPONSE" | grep HTTP_CODE | cut -d':' -f2)
  if [ "$HTTP_CODE" = "200" ]; then
    echo "[LOCAL] ✅ Requête collaborative réussie (200)"
  else
    echo "[LOCAL] ❌ Échec de la requête collaborative (HTTP $HTTP_CODE)"
    ERROR_OCCURRED=true
  fi
fi

# 👇 On quitte avec le bon code à la fin
if [ "$ERROR_OCCURRED" = true ]; then
   exit 1
fi
