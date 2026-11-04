FROM ubuntu:24.04
RUN apt-get update && apt-get install -y git
WORKDIR /app
RUN git init -b main \
 && git config user.email "a@b.c" && git config user.name "eval" \
 && git commit --allow-empty -m "initial"
