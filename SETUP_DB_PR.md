# 🎯 Configuration DB Partagée - Guide Complet

## ✅ Ce qui a été configuré

### 1. **Hooks Argo CD pour la gestion DB** 
📁 `kubernetes/helm/templates/db-pr-hooks.yaml`

- **PreSync Hook** : Crée la database `pr_XXX` et copie les données de prod
- **PreDelete Hook** : Supprime la database `pr_XXX` à la destruction de l'env

### 2. **Values Helm pour PR**
📁 `kubernetes/helm/values-pr.yaml`

- Database: `pr_{{ .Values.prNumber }}`
- Host: `city-api-prod-db` (instance PostgreSQL de prod)
- Copie des données de `city_api` (prod) au démarrage

### 3. **ApplicationSet Argo CD mis à jour**
📁 `kubernetes/argo-cd.yaml`

- Auto-création d'Applications pour chaque PR GitHub
- Namespace dédié par PR : `cityapi-pr-XXX`
- Finalizer pour exécuter les hooks de nettoyage

---

## 🚀 Comment ça fonctionne

### Architecture
```
┌─────────────────────────────────────────┐
│   PostgreSQL (city-api-prod-db)         │
│   Namespace: cityapi-prod               │
│                                         │
│   ├─ city_api (prod) ← données origine │
│   ├─ pr_123 ← copie de city_api        │
│   ├─ pr_124 ← copie de city_api        │
│   └─ pr_125 ← copie de city_api        │
└─────────────────────────────────────────┘
         ↑              ↑            ↑
         │              │            │
    cityapi-prod   cityapi-pr-123  cityapi-pr-124
    (ns: prod)     (ns: pr-123)    (ns: pr-124)
```

### Workflow complet

1. **PR ouverte sur GitHub**
   - GitHub Actions build l'image avec tag `pr-123`
   - Push sur `ghcr.io/aurianecodebien/cityapi:pr-123`

2. **Argo CD détecte la PR** (via ApplicationSet)
   - Crée l'Application `cityapi-pr-123`
   - Cible le namespace `cityapi-pr-123`

3. **PreSync Hook s'exécute**
   ```bash
   # Job Kubernetes qui se connecte à city-api-prod-db
   CREATE DATABASE pr_123 OWNER city_api;
   pg_dump city_api | psql pr_123  # Copie les données
   ```

4. **Déploiement de l'app**
   - Variables d'env :
     ```bash
     CITY_API_DB_HOST=city-api-prod-db
     CITY_API_DB_NAME=pr_123
     CITY_API_DB_URL=postgresql://city_api:city_api@city-api-prod-db:5432/pr_123
     ```

5. **PR fermée/mergée**
   - Argo CD supprime l'Application
   - **PreDelete Hook** s'exécute :
     ```bash
     DROP DATABASE IF EXISTS pr_123;
     ```

---

## 📋 Prérequis

### 1. Déployer la production d'abord

```bash
# Déployer l'instance PostgreSQL de prod
helm upgrade --install cityapi-prod ./kubernetes/helm \
  --namespace cityapi-prod \
  --create-namespace
```

Cela crée :
- PostgreSQL avec PVC
- Service `city-api-prod-db`
- Database `city_api`

### 2. Configurer Argo CD

```bash
# Installer l'ApplicationSet
kubectl apply -f kubernetes/argo-cd.yaml -n argocd
```

**Important** : Configurer le token GitHub dans Argo CD pour accéder aux PR.

---

## 🧪 Tester manuellement

### Déployer une PR test

```bash
# Exemple pour PR #123
helm upgrade --install cityapi-pr-123 ./kubernetes/helm \
  -f kubernetes/helm/values-pr.yaml \
  --set prNumber=123 \
  --set app.tag=pr-123 \
  --namespace cityapi-pr-123 \
  --create-namespace
```

### Vérifier la database

```bash
# Se connecter à PostgreSQL
kubectl exec -it deployment/city-api-prod-db -n cityapi-prod -- psql -U city_api -d postgres

# Lister les databases
\l

# Vérifier les données
\c pr_123
SELECT COUNT(*) FROM city;
```

### Nettoyer

```bash
# Supprimer l'env (déclenche le PreDelete hook)
helm uninstall cityapi-pr-123 -n cityapi-pr-123
kubectl delete namespace cityapi-pr-123
```

---

## ⚙️ Configuration GitHub Actions

Le workflow `.github/workflows/deploy-pr.yml` build l'image Docker pour chaque PR.

**Pour activer le déploiement K8s :**

1. Ajouter `KUBE_CONFIG` dans les secrets GitHub
2. Décommenter la section "Deploy to Kubernetes" dans le workflow

---

## 🔒 Sécurité

### Actuellement
- Credentials en clair dans `values.yaml`
- Acceptable pour dev/staging

### Pour la production
Utiliser des Kubernetes Secrets :

```yaml
# kubernetes/secrets/db-credentials.yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-credentials
  namespace: cityapi-prod
type: Opaque
stringData:
  username: city_api
  password: super-secret-password
```

Puis dans les values :
```yaml
db:
  user: city_api
  passwordSecret:
    name: db-credentials
    key: password
```

---

## 📊 Monitoring

### Vérifier les hooks Argo CD

```bash
# Voir les logs du hook PreSync
kubectl logs -n cityapi-pr-123 job/db-pr-init-123

# Voir les logs du hook PreDelete
kubectl logs -n cityapi-pr-123 job/db-pr-cleanup-123
```

### Dashboard Argo CD

Les hooks apparaissent dans l'interface Argo CD avec des icônes spéciales :
- 🔄 PreSync (avant le sync)
- 🗑️ PreDelete (avant la suppression)

---

## ❓ FAQ

### Q: Les PR peuvent-elles modifier la prod ?
**R:** Non, chaque PR a sa propre database isolée (`pr_XXX`).

### Q: Que se passe-t-il si la prod évolue pendant la vie de la PR ?
**R:** La PR garde sa copie initiale. Pour rafraîchir, supprimer et recréer l'env.

### Q: Peut-on avoir plusieurs PR en parallèle ?
**R:** Oui, chaque PR a sa database (`pr_123`, `pr_124`, etc.).

### Q: Comment gérer les migrations ?
**R:** Ajouter un Job PostSync qui lance les migrations après le déploiement.

---

## 🛠️ Dépannage

### La database PR n'est pas créée
```bash
# Vérifier les logs du hook
kubectl get jobs -n cityapi-pr-123
kubectl logs -n cityapi-pr-123 job/db-pr-init-123
```

### L'app ne se connecte pas
```bash
# Vérifier les variables d'env
kubectl get pod -n cityapi-pr-123
kubectl describe pod <pod-name> -n cityapi-pr-123 | grep -A 10 "Environment:"
```

### La database n'est pas supprimée
```bash
# Le finalizer doit être présent dans l'Application
kubectl get application cityapi-pr-123 -n argocd -o yaml | grep finalizers
```

---

## 📚 Fichiers importants

- `kubernetes/helm/templates/db-pr-hooks.yaml` - Hooks création/suppression DB
- `kubernetes/helm/values-pr.yaml` - Configuration PR
- `kubernetes/argo-cd.yaml` - ApplicationSet auto-PR
- `kubernetes/DATABASE.md` - Documentation DB
- `.github/workflows/deploy-pr.yml` - CI/CD PR
