FROM python:3.9

WORKDIR /app

ENV PYTHONPATH=/app


# Copiamos los requerimientos para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto incluyendo la carpeta data y scripts
COPY . .

# El comando que ejecutara la ingesta
CMD ["python", "scripts/ingesta.py"]
