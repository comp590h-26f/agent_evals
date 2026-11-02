FROM python:3.12-slim-bookworm

RUN python -m pip install --no-cache-dir pytest==9.1.1

WORKDIR /app
COPY next.py /app/next.py
COPY generate_chain.py /tmp/generate_chain.py
RUN PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/app python /tmp/generate_chain.py \
    && rm /tmp/generate_chain.py
