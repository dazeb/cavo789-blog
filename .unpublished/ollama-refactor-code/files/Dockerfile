# syntax=docker/dockerfile:1
FROM python:3.14-alpine

# 1. On récupère le binaire 'uv' depuis l'image officielle (très léger)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 2. Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPYCACHEPREFIX=/tmp/pycache \
    # UV utilise ce dossier pour le cache
    UV_CACHE_DIR=/tmp/uv-cache

WORKDIR /app

# 3. Installation des dépendances système
RUN apk add --no-cache git

# 4. Installation des dépendances Python via UV
# On utilise BuildKit pour le cache de 'uv'
# --frozen garantit que tu utilises exactement les versions prévues
COPY pyproject.toml ./
# Si tu as un uv.lock, copie-le aussi : COPY uv.lock ./

RUN --mount=type=cache,target=/tmp/uv-cache \
    uv pip install --system --requirement pyproject.toml

# 5. Sécurité : On crée un utilisateur non-root
RUN adduser -D appuser && \
    mkdir -p /tmp/pycache && \
    chmod 777 /tmp/pycache
    
USER appuser

# 6. Copie des sources
COPY --chown=appuser:appuser src/ ./src/
COPY --chown=appuser:appuser config/ ./config/

ENTRYPOINT ["python", "src/main.py"]