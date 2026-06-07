# Etapa 1: build
FROM python:3.12-slim AS builder
WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        python3-dev \
        gcc \
        libssl-dev \
        libffi-dev \
        curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --user -r requirements.txt

# Etapa 2: execução
FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:${PORT}"]