FROM python:3.12-slim-bookworm

RUN python -m pip install --no-cache-dir pytest==9.1.1

WORKDIR /app
COPY invoice.py /app/invoice.py
COPY skills /skills
