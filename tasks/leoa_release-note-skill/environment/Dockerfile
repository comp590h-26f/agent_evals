FROM python:3.12-slim-bookworm

RUN python -m pip install --no-cache-dir pytest==9.1.1

COPY skills/ /root/.claude/skills/
COPY skills/ /root/.agents/skills/
WORKDIR /app
