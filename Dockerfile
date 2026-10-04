# Etapa 1: compila o frontend (React + Vite)
FROM node:22-alpine AS frontend
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# Etapa 2: backend FastAPI que tambem entrega o site compilado
FROM python:3.13-slim
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STATIC_DIR=/app/static
WORKDIR /app

COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app ./app
COPY backend/content ./content
COPY --from=frontend /frontend/dist ./static

# o container nao roda como root; a pasta de cache guarda a ultima lista boa de projetos e posts
# (no servidor ela fica em um volume, para sobreviver aos reinicios)
RUN useradd --system --no-create-home app && mkdir -p /app/cache && chown app /app/cache
ENV CACHE_DIR=/app/cache
USER app

EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health')" || exit 1

# --proxy-headers: atras do Cloudflare/nginx o IP e o protocolo reais chegam pelos cabecalhos
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
