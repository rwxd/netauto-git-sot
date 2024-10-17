from python:3.13-slim

RUN : \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        python3 \
        python3-venv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN : \
    && python3 -m venv /venv \
    && pip --no-cache-dir install -r requirements.txt

COPY requirements.yml .

RUN ansible-galaxy collection install -r requirements.yml

COPY . .

RUN python3 -m eve --install-completion bash

ENTRYPOINT ["python3", "-m", "eve"]

