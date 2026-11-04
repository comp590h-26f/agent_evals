FROM ubuntu:24.04

# Install or copy over any environment dependencies here.

RUN python -m pip install --no-cache-dir pytest==9.1.1

WORKDIR /app
COPY calculator.py /app/calculator.py
