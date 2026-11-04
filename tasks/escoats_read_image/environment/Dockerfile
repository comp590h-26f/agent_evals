FROM python:3.12-slim-bookworm

RUN python -m pip install --no-cache-dir pytest==9.1.1

WORKDIR /app
COPY number.png /app/number.png
COPY answer.txt /app/answer.txt