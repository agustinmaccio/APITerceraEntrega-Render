# Usar una imagen base de Python
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos a la imagen
COPY requirements.txt .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente de la aplicación
COPY . .

# Comando para iniciar la aplicación
CMD ["gunicorn", "--worker-tmp-dir", "/dev/shm", "APITerceraEntrega.wsgi:application", "--bind", "0.0.0.0:10000"]
