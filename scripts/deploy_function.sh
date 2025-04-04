#!/bin/bash
set -e

if [ "$GH_CI" = "true" ]; then
  cd azure_function
  func azure functionapp publish "$AZURE_FUNCTION_NAME" --python
else
  echo "Skipping Azure Function deployment (GH_CI != true)"
fi

