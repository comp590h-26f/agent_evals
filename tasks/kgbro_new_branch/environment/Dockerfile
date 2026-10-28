FROM python:3.12-slim-bookworm

RUN apt-get update \
    && apt-get install -y --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --no-cache-dir pytest==9.1.1

WORKDIR /app
COPY calculator.py /app/calculator.py

RUN git init --initial-branch=main \
    && git config user.name "Task" \
    && git config user.email "task@example.com" \
    && git add calculator.py \
    && git commit -m "Add calculator starter"
