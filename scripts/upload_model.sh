#!/bin/bash
set -e

MODEL_NAME=$1

if [ "$GH_CI" = "true" ]; then
  echo "🚀 Uploading $MODEL_NAME to Azure Blob Storage..."
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
