# --- Build stage ---
FROM python:3.12-slim AS builder

WORKDIR /app

# Dependências de sistema para mysqlclient e Pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --prefix=/install -r requirements.txt


# --- Runtime stage ---
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings.prod

WORKDIR /app

# Dependências de runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-libmysqlclient-dev \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia pacotes instalados do builder
COPY --from=builder /install /usr/local

# Copia o código-fonte
COPY . .

# Cria diretórios necessários
RUN mkdir -p logs media staticfiles

# Variáveis dummy apenas para o collectstatic (não precisa de banco real)
ARG SECRET_KEY=build-dummy-secret-key
ARG DB_NAME=dummy
ARG DB_USER=dummy
ARG DB_PASSWORD=dummy
ARG DB_HOST=dummy
ARG EMAIL_HOST_USER=dummy@dummy.com
ARG EMAIL_HOST_PASSWORD=dummy

ENV SECRET_KEY=${SECRET_KEY} \
    DB_NAME=${DB_NAME} \
    DB_USER=${DB_USER} \
    DB_PASSWORD=${DB_PASSWORD} \
    DB_HOST=${DB_HOST} \
    EMAIL_HOST_USER=${EMAIL_HOST_USER} \
    EMAIL_HOST_PASSWORD=${EMAIL_HOST_PASSWORD}

# Coleta os arquivos estáticos
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Entrypoint: aguarda o banco, roda migrate e sobe o Gunicorn
CMD ["sh", "-c", "\
    python manage.py migrate --noinput && \
    gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout 120 \
        --access-logfile - \
        --error-logfile - \
"]
