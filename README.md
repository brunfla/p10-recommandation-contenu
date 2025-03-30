# p10-recommandation-contenu

## Administration

###
```bash
az ad sp create-for-rbac \
  --name "gh-deploy-sp" \
  --role contributor \
  --scopes /subscriptions/XXX/resourceGroups/XXX \
  --sdk-auth
```
