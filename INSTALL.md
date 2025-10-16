# Guide d'installation de CityAPI

Ce guide décrit comment lancer l'application **CityAPI** avec :

- Docker Compose (local, rapide)
- Helm sur un cluster Kubernetes (via K3s)

---

## Déploiement avec Argo-CD (environements éphémères automatiques)

### 1. Initialiser un cluster Kubernetes
https://docs.k3s.io/quick-start
`curl -sfL https://get.k3s.io | sh -`

`kubectl create namespace cityapi`

### 2. Installer Argo-CD
```bash

```

### 3. Déployer ApplicationSet
`kubectl -n cityapi apply -f kubernetes/base/argo-cd.yaml`

Note: l'ApplicationSet lui-même n'est pas deployé par argo-cd pour éviter les effets de bords entre les différentes PR.


## Installation avec Docker Compose

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

## Déploiement avec Helm (Kubernetes)

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

## Installation du chart Helm `city-api`

Pour déployer l'application avec Helm sur un cluster :

1. Assurez-vous que votre cluster est en ligne (`kubectl get nodes`).
2. Placez-vous dans le dossier du projet.
3. Installez le chart avec vos valeurs :

```bash
helm install cityapi ./helm -f values.yaml
```

Pour mettre à jour ensuite :

```bash
helm upgrade cityapi ./helm -f values.yaml
```

## Prometheus et Dashboard Grafana

Nous avons configuré Grafana dans le `docker-compose.yml` afin de permettre la visualisation des métriques de l'application exposées via Prometheus.

- Un service Grafana est lancé sur le port `3000`
- Prometheus est configuré comme source de données
- Le dashboard Grafana affiche le temps CPU utilisé par l'application Flask

> Cela permet de suivre en temps réel l’activité de l’API et de détecter les anomalies.



## CI/CD

La CI/CD a été mise en place via GitHub Actions dans le dossier `.github/workflows`.

### Étapes automatisées :

- **Lint (Super-Linter)** : vérifie le code à chaque push.
- **Tests (pytest)** : exécute les tests unitaires avec `pytest`.
- **Build Docker** : build de l'image avec `Dockerfile`.
- **Push DockerHub** : push automatique de l’image `city-api:latest`.
- **Tag & Versioning** : si un tag `vX.X.X` est détecté, une image versionnée `city-api:X.X.X` est poussée.
- **Scan de sécurité** : un scan CVE avec `trivy` est effectué.
- **Release** : un job spécifique est déclenché sur les tags versionnés.


## Explication appli Flask

L'application a été développée avec **Flask** et **SQLAlchemy**. Elle expose une API REST qui permet de :

- Ajouter une ville (`POST /city`)
- Ajouter plusieurs villes (`POST /cities`)
- Récupérer toutes les villes (`GET /city`)
- Vérifier l'état de l'API (`GET /_health`)
- Exporter des métriques Prometheus (`GET /metrics`)

### Structure du projet :

```bash
CityApi/
├── app/
│   ├── app.py               # Création de l'app Flask
│   ├── extensions.py        # Initialisation de SQLAlchemy
│   ├── models/
│   │   └── city.py          # Définition de la table City
│   └── routes/
│       ├── city.py          # Routes /city et /cities
│       ├── health.py        # Route /_health
│       └── metrics.py       # Route /metrics
├── run.py                  # Point d'entrée (app.run)
├── Dockerfile             # Build de l’image
├── docker-compose.yml     # Déploiement local DB + API + monitoring
├── init.sql               # Script SQL pour initialiser la base
├── requirements.txt       # Dépendances pour exécution hors-poetry
├── pyproject.toml         # Dépendances via poetry
└── tests/                 # Tests unitaires pytest
```

L'application est entièrement configurable via les variables d’environnement :

- `CITY_API_ADDR`
- `CITY_API_PORT`
- `CITY_API_DB_URL`
- `CITY_API_DB_USER`
- `CITY_API_DB_PWD`
