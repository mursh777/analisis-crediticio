FROM python:3.9

WORKDIR /app

ENV PYTHONPATH=/app


# Copiamos los requerimientos 
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del proyecto incluyendo la carpeta data y src
COPY . .

# El comando que ejecutara la ingesta
CMD ["python", "src/ingesta/ingesta.py"]
