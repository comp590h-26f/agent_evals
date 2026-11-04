FROM python:3.12-slim-bookworm

RUN python -m pip install --no-cache-dir pytest==9.1.1

WORKDIR /app
COPY release_data.json /app/release_data.json
COPY skills /app/skills
