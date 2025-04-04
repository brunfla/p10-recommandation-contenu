#!/bin/bash
set -e

if [ "$GH_CI" = "true" ]; then
  azcopy copy data/outs/model/model_svd.pkl "$MODEL_SAS_URL" --overwrite=true
else
  echo "Skipping upload"
fi
