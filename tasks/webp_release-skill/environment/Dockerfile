FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --no-cache-dir pytest==9.1.1

RUN git config --global user.name "Tally Maintainer" \
    && git config --global user.email "maintainer@example.com" \
    && git config --global init.defaultBranch main \
    && git config --global --add safe.directory /app

WORKDIR /app
COPY app /app
RUN git init -q && git add -A && git commit -qm "Initial commit"
