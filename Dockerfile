# Dockerfile para BIOptimization
FROM python:3.11-slim

# Definir variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar codigo fuente del proyecto
COPY . .

# Comando por defecto
CMD ["python", "main.py"]
