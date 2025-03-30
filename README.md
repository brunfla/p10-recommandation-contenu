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
