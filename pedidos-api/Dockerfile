# Etapa 1: build
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

# Etapa 2: execução
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
ENV PORT=8000
EXPOSE 8000
CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:${PORT}"]