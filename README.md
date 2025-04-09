# Rapport CI/CD du projet CityAPI
- Estelle TAMALET
- Auriane PUSEL
- Ruben ROUVIÈRE


## 🌐 Dépôt GitHub
Lien vers le dépôt GitHub : [https://github.com/aurianecodebien/CityApi/](https://github.com/aurianecodebien/CityApi/)

---

## [Lien vers le guide d'installation](./INSTALL.md)

---

## ⛏ Prérequis installés
- [x] Docker
- [x] Docker Compose
- [x] Python 3.11
- [x] Poetry

---

## 🚧 Infrastructure avec Docker Compose
Deux services sont définis :
- **db** : s'appuie sur l'image `postgres:latest`
- **app** : notre API Python


## 🌐 API Web en Python

**Framework** : **Flask + SQLAlchemy**  
**Gestion des variables** via `python-dotenv`

### Endpoints implémentés

| Méthode   | URI          | Rôle                                |
|-----------|--------------|-------------------------------------|
| `GET`     | `/city`      | Liste les villes                    |
| `POST`    | `/city`      | Ajoute une ville (via JSON)         |
| `GET`     | `/_health`   | Retourne 204 si la DB répond        |
| `GET`     | `/metrics`   | Expose les métriques Prometheus     |

## ⚖️ Tests automatisés (`pytest`)

### 1. `test_insert_bd.py`
- Vérifie l'ajout d'une ville en base
- Vérifie la route `/city` (`GET`)

### 2. `test_health.py`
- Vérifie la route `/_health`

#### Lancement local :
```bash
cd test
pytest
```


## 📅 GitHub Actions CI/CD

### ✅ Lint (Super-Linter)
- S'exécute à chaque `push`

### ✅ Tests (Pytest)
- Lance automatiquement `pytest`

### ✅ Build Docker
- Build de l'image `city-api`

### ✅ Scan de sécurité (CVE)
- Ajout d'un scan trivy sur chaque image buildée

### ✅ Versioning
- Sur `tag` au format `vX.X.X`, push d'une image taggée `city-api:X.X.X`

### ✅ Push sur DockerHub
- Push de l'image `city-api:latest` sur DockerHub

## 🌌 Monitoring Prometheus + Grafana

Ajout dans `docker-compose.yml` :

- Service **prometheus** avec scrape de `app:2022/metrics`
- Service **grafana** avec dashboard préconfiguré



## ✨ Déploiement Kubernetes

1. Installation de K3s localement
2. Déploiement via Helm Chart
3. Exposition des routes avec un Ingress
4. Configuration des `values.yaml`

## 📊 Exposition de métriques

- `/metrics` exposé via `prometheus_flask_exporter`


## 🐞 Blocages rencontrés et résolutions

### 1. Super-Linter et les templates Helm (Jinja2)

**Problème** :  
Le linter GitHub Actions (`super-linter`) échouait sur les fichiers Helm car ceux-ci utilisent la syntaxe Jinja2 (`{{ }}`), qui n'est pas comprise par défaut par les linters YAML.

**Solution** :  
Nous avons exclu les fichiers Helm du linting automatique en adaptant la configuration afin d’éviter l’analyse par Super-Linter, tout en maintenant un bon formatage dans le reste du projet.

## 📄 Checklist

- [x] API REST conforme au format JSON attendu
- [x] Base PostgreSQL pilotée via Docker
- [x] Pipelines CI/CD complètes avec lint, tests, build, push et sécurité
- [x] Monitoring et déploiement K3s finalisé

