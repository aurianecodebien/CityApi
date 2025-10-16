# 🗄️ Configuration Database PostgreSQL Partagée

## Architecture

```
┌────────────────────────────────────┐
│   PostgreSQL (city-api-prod-db)    │
│                                    │
│   ├─ city_api (prod)               │
│   ├─ pr_123 (PR #123)              │
│   ├─ pr_124 (PR #124)              │
│   └─ pr_125 (PR #125)              │
└────────────────────────────────────┘
         ↑           ↑          ↑
         │           │          │
    cityapi-prod  pr-123    pr-124
```

**Une seule instance PostgreSQL**, plusieurs databases :
- **Production** : utilise `city_api` (base par défaut)
- **PR éphémères** : chaque PR a sa propre database `pr_XXX` avec une **copie des données de prod**

## 🚀 Déploiement Production

```bash
# Déployer l'app + DB de prod
helm upgrade --install cityapi-prod ./kubernetes/helm \
  --namespace cityapi-prod \
  --create-namespace
```

Cela crée :
- Deployment PostgreSQL avec PVC
- Service `city-api-prod-db`
- Database `city_api`
- App qui se connecte à `city_api`

## 🧪 Déploiement PR Éphémère

```bash
# Exemple pour la PR #123
helm upgrade --install cityapi-pr-123 ./kubernetes/helm \
  -f ./kubernetes/helm/values-pr.yaml \
  --set prNumber=123 \
  --set app.tag=pr-123 \
  --namespace cityapi-pr-123 \
  --create-namespace
```

Cela :
1. **PreSync Hook** : Crée la database `pr_123` et copie les données de `city_api`
2. Déploie l'app qui se connecte à `city-api-prod-db` avec `db=pr_123`
3. **PreDelete Hook** : Supprime la database `pr_123` quand l'env est détruit

## 🔧 Variables d'environnement

L'app reçoit :
```bash
CITY_API_DB_HOST=city-api-prod-db
CITY_API_DB_PORT=5432
CITY_API_DB_NAME=pr_123          # ou "city_api" pour prod
CITY_API_DB_USER=city_api
CITY_API_DB_PWD=city_api
CITY_API_DB_URL=postgresql://city_api:city_api@city-api-prod-db:5432/pr_123
```

## 📋 Workflow GitHub Actions (exemple)

```yaml
name: Deploy PR Environment

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  deploy-pr:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Deploy to K8s
        run: |
          PR_NUMBER=${{ github.event.pull_request.number }}
          
          helm upgrade --install cityapi-pr-${PR_NUMBER} ./kubernetes/helm \
            -f ./kubernetes/helm/values-pr.yaml \
            --set prNumber=${PR_NUMBER} \
            --set app.tag=pr-${PR_NUMBER} \
            --namespace cityapi-pr-${PR_NUMBER} \
            --create-namespace
```

## 🗑️ Nettoyage PR

Quand la PR est fermée ou mergée, supprimer l'environnement :

```bash
helm uninstall cityapi-pr-123 --namespace cityapi-pr-123
kubectl delete namespace cityapi-pr-123
```

Le hook `PreDelete` supprimera automatiquement la database `pr_123`.

## ⚠️ Important

- Les PR partagent la **même instance PostgreSQL** que la prod
- Chaque PR a sa **propre database** isolée
- Les données sont **copiées de prod au démarrage**
- Les modifications dans les PR **n'affectent PAS la prod**
- Penser à gérer les **migrations** si les schemas diffèrent entre PR et prod

## 🔐 Sécurité

Pour la production, remplacer les credentials par des Secrets Kubernetes :

```yaml
# kubernetes/helm/values.yaml
db:
  user: city_api
  password: ${DB_PASSWORD}  # À injecter via Secret
```
