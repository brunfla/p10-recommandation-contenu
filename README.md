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

## DVC

### 📦 `dvc pull` – Options disponibles
| Option                       | Description                                                                                                                                       | Quand l’utiliser                                                                                      |
|-----------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| `-h`, `--help`              | Affiche l’aide                                                                                                                                     | Pour voir la documentation de la commande                                                            |
| `-q`, `--quiet`             | Mode silencieux                                                                                                                                    | Pour réduire le bruit dans les logs CI                                                               |
| `-v`, `--verbose`           | Mode verbeux                                                                                                                                       | Pour debug ou comprendre ce que fait DVC                                                              |
| `-j <number>`               | Nombre de jobs en parallèle (ex: `-j 4`)                                                                                                            | Optimise les performances de download (ex: S3 ou GCS avec plusieurs threads)                         |
| `-r <name>`                 | Nom de la remote à utiliser                                                                                                                        | Si tu as plusieurs remotes DVC et veux cibler une en particulier                                     |
| `-a`, `--all-branches`      | Télécharge le cache pour toutes les branches                                                                                                       | Pour des workflows multi-branches                                                                    |
| `-T`, `--all-tags`          | Télécharge le cache pour tous les tags                                                                                                             | Pour préremplir le cache de release/tag                                                             |
| `-A`, `--all-commits`       | Télécharge le cache de tous les commits                                                                                                            | Pour rebuild un cache complet en local                                                               |
| `-f`, `--force`             | Ignore les prompts et écrase les fichiers s’ils existent                                                                                           | Utile en CI pour ne pas avoir d’interruption                                                         |
| `-d`, `--with-deps`         | Tire les fichiers *dépendants* aussi (via `deps:` dans les stages)                                                                                 | Quand tu pulls un stage ou un fichier `.dvc` spécifique, et veux aussi les deps associés              |
| `-R`, `--recursive`         | Récursif sur un répertoire donné                                                                                                                    | Pour pull tous les fichiers `.dvc` dans un dossier et ses sous-dossiers                              |
| `--run-cache` / `--no-run-cache` | Télécharge (ou non) le cache d’exécution (`run-cache`)                                                                                     | Pour CI, parfois utile d’avoir la trace des runs antérieurs                                          |
| `--allow-missing`           | Ignore les erreurs si des fichiers sont manquants dans la remote                                                                                   | Utile pour éviter que le pipeline crash quand certains outputs ne sont pas encore dans le remote     |
| `targets` (positional)      | Les fichiers, stages ou `.dvc` spécifiques à pull                                                                                                  | Pour cibler des fichiers précis (ex: `data/train.dvc`, ou un nom de stage comme `train_model`)       |


### Ajouter les dépendances DVC
```bash
dvc add data/deps/articles_metadata.csv
dvc add data/deps/clicks_sample.csv
# dvc add data/outs/model/model_svd.pkl
```

### Génère le hash des secrets
# ```bash
# echo -n "$MODEL_SAS_URL" | sha256sum | cut -d ' ' -f1 > data/deps/.github/MODEL_SAS_URL.hash
# dvc add data/deps/.github/MODEL_SAS_URL.hash
# ```

# ```bash
# echo -n "$AZURE_RESOURCE_GROUP" | sha256sum | cut -d ' ' -f1 > data/deps/.github/AZURE_RESOURCE_GROUP.hash
# dvc add data/deps/.github/AZURE_RESOURCE_GROUP.hash
# ```

# ```bash
# echo -n "$AZURE_FUNCTION_NAME" | sha256sum | cut -d ' ' -f1 > data/deps/.github/AZURE_FUNCTION_NAME.hash
# dvc add data/deps/.github/AZURE_FUNCTION_NAME.hash
# ```
