# Utiliser une image Python légère avec Poetry préinstallé
FROM python:3.11-slim

WORKDIR /app
EXPOSE 2022

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root

COPY ./app .


# Spécifier la commande pour démarrer l'application
CMD ["poetry", "run", "python", "app.py"]
