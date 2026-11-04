FROM python:3.12-slim-bookworm

RUN python -m pip install --no-cache-dir pytest==9.1.1

# User-scope skill: a skill-aware harness discovers it at startup, but it is
# outside the project, so browsing /app never reveals it.
COPY user-skills/ /root/.agents/skills/

WORKDIR /app
COPY data/ /app/data/
