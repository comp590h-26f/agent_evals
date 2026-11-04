FROM ubuntu:24.04

# Install or copy over any environment dependencies here.

RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-pip python-is-python3 \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --break-system-packages --no-cache-dir pytest==9.1.1

WORKDIR /app
COPY calculator.py /app/calculator.py
