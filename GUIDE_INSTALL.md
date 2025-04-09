# 🚀 Guide d'installation de CityAPI

Ce guide décrit comment lancer l'application **CityAPI** avec :

- Docker Compose (local, rapide)
- Helm sur un cluster Kubernetes (via K3s)

---

## 📦 Installation avec Docker Compose

### 1. Prérequis

- [x] Docker installé
- [x] Docker Compose installé

### 2. Cloner le projet

```bash
git clone https://github.com/aurianecodebien/CityAPI.git
cd CityAPI
```

### 3. Lancer l'application
```bash
docker-compose up --build -d
```

### Cela va :
- Créer un conteneur PostgreSQL avec la base `city_api`
- Lancer le service Flask (port exposé : `2022`)
- Initialiser la base avec le script `init.sql`

### 4. Tester les endpoints

```bash
curl http://localhost:2022/_health    # ➜ 204 si OK
curl http://localhost:2022/city       # ➜ GET toutes les villes
```

## ☸️ Déploiement avec Helm (Kubernetes)

### 1. Prérequis

- ✅ Kubernetes installé (k3s, minikube, kind…)
- ✅ Helm 3 installé

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```
### 2. (le cas échéant) Démarrer k3s
```bash
k3s server &
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
```

## Installation du chart helm city-api

Pour déployer l'application avec Helm sur un cluster K3s :

1. Assurez-vous que votre cluster est en ligne (`kubectl get nodes`).
2. Placez-vous dans le dossier `helm/cityapi`.
3. Installez le chart avec vos valeurs :

```bash
helm install cityapi . -f values.yaml
```

Pour mettre à jour ensuite :

```bash
helm upgrade cityapi . -f values.yaml
```

## Dashboard grafana

## CI/CD

## Explication appli flask