FROM python:3.12-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*
RUN python -m pip install --no-cache-dir pytest==9.1.1

WORKDIR /app
COPY login.py /app/login.py
COPY skills/ /app/.agents/skills/
RUN git init -q && git config user.name "Eval Fixture" \
    && git config user.email "fixture@example.invalid" \
    && git add login.py .agents && git commit -qm "Add login handler" \
    && sed -i 's/if not verify_password/if verify_password/' login.py \
    && git add login.py
