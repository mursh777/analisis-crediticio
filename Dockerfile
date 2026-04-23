FROM python:3.9-slim

# Instalamos dependencias del sistema necesarias para compilar psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiamos primero los requerimientos para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto (incluyendo la carpeta data y scripts)
COPY . .

# El comando que ejecutará tu ingesta
CMD ["python", "scripts/ingesta.py"]
