# p10-recommandation-contenu

## Administration

### Creation des credentials Azure
```bash
az ad sp create-for-rbac \
  --name "gh-deploy-sp" \
  --role contributor \
  --scopes /subscriptions/XXX/resourceGroups/XXX \
  --sdk-auth
```

### Recompilation de requirements.txt
```bash
pip-compile requirements.in
```

### Ajouter les dépendances DVC
```bash
dvc add data/deps/articles_metadata.csv
dvc add data/deps/clicks_sample.csv
```

### Génère le hash des secrets
```bash
echo -n "$MODEL_SAS_URL" | sha256sum | cut -d ' ' -f1 > data/deps/.github/MODEL_SAS_URL.hash
dvc add data/deps/.github/MODEL_SAS_URL.hash
```

```bash
echo -n "$AZURE_RESOURCE_GROUP" | sha256sum | cut -d ' ' -f1 > data/deps/.github/AZURE_RESOURCE_GROUP.hash
dvc add data/deps/.github/AZURE_RESOURCE_GROUP.hash
```

```bash
echo -n "$AZURE_FUNCTION_NAME" | sha256sum | cut -d ' ' -f1 > data/deps/.github/AZURE_FUNCTION_NAME.hash
dvc add data/deps/.github/AZURE_FUNCTION_NAME.hash
```
