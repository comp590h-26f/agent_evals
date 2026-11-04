FROM python:3.12-slim-bookworm

RUN python -m pip install --no-cache-dir pytest==9.1.1

WORKDIR /app
# User-level Agent Skill, in the cross-client ~/.agents/skills/ location.
COPY .agents /root/.agents
