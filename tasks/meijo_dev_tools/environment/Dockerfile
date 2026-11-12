FROM python:3.12-slim-bookworm

RUN python -m pip install --no-cache-dir pytest==9.1.1

WORKDIR /app
COPY project-note.txt /app/project-note.txt
COPY .agents /app/.agents
