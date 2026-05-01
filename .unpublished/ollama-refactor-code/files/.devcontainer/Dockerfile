# syntax=docker/dockerfile:1
FROM python:3.14-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 1. Installation de sudo en plus des autres outils
RUN apk add --no-cache \
    git bash curl libstdc++ gcompat openssh-client shadow sudo

# 2. Création de l'utilisateur vscode
RUN addgroup -S vscode && \
    adduser -S vscode -G vscode -s /bin/bash


# 3. Configuration de SUDO sans mot de passe pour vscode (Crucial pour Alpine)
RUN echo "vscode ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/vscode && \
    chmod 0440 /etc/sudoers.d/vscode

# 4. On pré-crée les dossiers de cache
RUN mkdir -p /tmp/pycache /tmp/uv-cache && \
    chown -R vscode:vscode /tmp/pycache /tmp/uv-cache

WORKDIR /app

ENV UV_LINK_MODE=copy \
    UV_CACHE_DIR=/tmp/uv-cache \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPYCACHEPREFIX=/tmp/pycache

USER vscode