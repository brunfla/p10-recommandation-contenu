#!/bin/bash
set -e

if [ "$GH_CI" = "true" ]; then
  echo "🚀 Déploiement Azure Function : P10"
  cd azure_function && func azure functionapp publish "P10" --python
else
  echo "🧪 Dev local – démarrage des fonctions en local..."

  mkdir -p .dvc/tmp
  cd azure_function

  func start -p 7072 --verbose &
fi
