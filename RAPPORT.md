# Rapport CI/CD du projet CityAPI

## 🌐 Dépôt GitHub
Lien vers le dépôt GitHub : [https://github.com/aurianecodebien/CityApi/](https://github.com/aurianecodebien/CityApi/)

---

## ⛏ Prérequis installés
- [x] Docker
- [x] Docker Compose
- [x] Python 3.11
- [x] Poetry

---

## 🚧 Infrastructure avec Docker Compose

### Fichier `docker-compose.yml`
Deux services sont définis :
- **db** : s'appuie sur l'image `postgres:latest`
- **app** : notre API Python

```yaml
version: '3.8'

services:
  db:
    image: postgres
    environment:
      POSTGRES_DB: city_api
      POSTGRES_USER: city_api
      POSTGRES_PASSWORD: city_api
    ports:
      - "5432:5432"
    volumes:
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
      - city_api_data:/var/lib/postgresql/data

  app:
    build:
      context: .
      dockerfile: Dockerfile
    depends_on:
      - db
    environment:
      CITY_API_ADDR: "0.0.0.0"
      CITY_API_PORT: "2022"
      CITY_API_DB_URL: "db:5432/city_api"
      CITY_API_DB_USER: "city_api"
      CITY_API_DB_PWD: "city_api"
    ports:
      - "2022:2022"

volumes:
  city_api_data:
```

### Fichier `init.sql`
Initialisation de la table city :

```sql
CREATE TABLE IF NOT EXISTS city (
  id SERIAL PRIMARY KEY,
  department_code VARCHAR NOT NULL,
  insee_code VARCHAR,
  zip_code VARCHAR,
  name VARCHAR NOT NULL,
  lat FLOAT NOT NULL,
  lon FLOAT NOT NULL
);
```

## 🌐 API Web en Python

**Framework** : **Flask + SQLAlchemy**  
**Gestion des variables** via `python-dotenv`

### Endpoints implémentés

| Méthode | URI        | Rôle                                |
|---------|------------|-------------------------------------|
| GET     | /city      | Liste les villes                    |
| POST    | /city      | Ajoute une ville (via JSON)         |
| GET     | /_health   | Retourne 204 si la DB répond        |
| GET     | /metrics   | Expose les métriques Prometheus     |

## ⚖️ Tests automatisés (pytest)

### 1. `test_insert_bd.py`
- Vérifie l'ajout d'une ville en base
- Vérifie la route `/city` (GET)

### 2. `test_health.py`
- Vérifie la route `/_health`

#### Lancement local :
```bash
pytest
```

## 🛠️ Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app
EXPOSE 2022

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY ./run.py .
COPY ./app ./app

CMD ["poetry", "run", "python", "run.py"]
```

## 📅 GitHub Actions CI/CD

### ✅ Lint (Super-Linter)
- S'exécute à chaque `push`

### ✅ Tests (Pytest)
- Lance automatiquement `pytest`

### ✅ Build Docker
- Build de l'image `city-api`

### ✅ Push sur DockerHub
- Push de l'image `city-api:latest` sur DockerHub

### ✅ Versioning
- Sur `tag` au format `vX.X.X`, push d'une image taggée `city-api:X.X.X`

### ✅ Scan de sécurité (CVE)
- Ajout d'un scan trivy sur chaque image buildée

## 🌌 Monitoring Prometheus + Grafana

Ajout dans `docker-compose.yml` :

- Service **prometheus** avec scrape de `app:2022/metrics`
- Service **grafana** avec dashboard préconfiguré



## ✨ Déploiement Kubernetes avec K3s

1. Installation de K3s localement
2. Déploiement via Helm Chart
3. Exposition des routes avec un Ingress
4. Configuration des `values.yaml`

## 📊 Exposition de métriques

- `/metrics` exposé via `prometheus_flask_exporter`



## 📄 Conclusion

Ce projet CI/CD respecte l'ensemble des consignes :

- API REST conforme au format JSON attendu
- Base PostgreSQL pilotée via Docker
- Pipelines CI/CD complètes avec lint, tests, build, push et sécurité
- Monitoring et déploiement K3s finalisé

> Un travail collaboratif de qualité avec les bonnes pratiques DevOps.



## 📅 Collaborateurs

- **Estelle TAMALET**
- **Auriane PUSEL**
- **Ruben ROUVIERE**

