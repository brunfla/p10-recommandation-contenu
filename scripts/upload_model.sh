#!/bin/bash
set -e

MODEL_NAME=$1

if [ "$GH_CI" = "true" ]; then
  echo "🚀 Uploading $MODEL_NAME to Azure Blob Storage..."
  # Détermine si c'est content-based ou collaborative
  if [[ "$MODEL_NAME" == *"content"* ]]; then
    MODEL_SAS_URL="https://bflament.blob.core.windows.net/p10/prod/content_based_model.pkl?sp=racwdyti&st=2025-04-16T19:06:09Z&se=2025-04-18T03:06:09Z&spr=https&sv=2024-11-04&sr=b&sig=xiyY%2F12rJDuSpe8cQn2VtD5dCw%2Fkgy5VPnRq5SkwuwI%3D"
  else
    MODEL_SAS_URL="https://bflament.blob.core.windows.net/p10/prod/collaborative_filtering_svd.pkl?sp=racwdyti&st=2025-04-16T18:39:29Z&se=2025-04-21T02:39:29Z&sv=2024-11-04&sr=b&sig=9JD6EDN9quUQeRVKaGocmEYO1IaI56RECTp6J%2B8Rz7Q%3D"
  fi

  azcopy copy data/outs/model/$MODEL_NAME "$MODEL_SAS_URL" --overwrite=true

else
  echo "📦 Running locally – copying $MODEL_NAME to Azure Function shared/ folder..."

  # Détermine si c'est content-based ou collaborative
  if [[ "$MODEL_NAME" == *"content"* ]]; then
    TARGET_DIR="azure_function/content_based_model/shared"
  else
    TARGET_DIR="azure_function/collaborative_filtering_model/shared"
  fi

  mkdir -p "$TARGET_DIR"
  cp "data/outs/model/$MODEL_NAME" "$TARGET_DIR/"

  echo "✅ Copied to $TARGET_DIR"
fi
