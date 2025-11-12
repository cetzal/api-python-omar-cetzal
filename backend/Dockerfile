# Imagen base ligera de Python
FROM python:3.11-slim

# Crea carpeta de trabajo dentro del contenedor
WORKDIR /app

# Evita que Python genere archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copia el archivo de dependencias si existe
COPY requirements.txt .

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt || true

# Copia el código del proyecto
COPY . .

# Hace el entrypoint ejecutable
RUN chmod +x /app/install.sh

# Comando por defecto (ejecuta migraciones y crea el usuario demo antes de iniciar el servidor)
# ENTRYPOINT ["/app/install.sh"]
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
