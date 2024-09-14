# Usa una imagen base de Python
FROM python:3.10-slim-bullseye

# Crear un entorno virtual
RUN python -m venv /opt/env

# Activar el entorno virtual
ENV PATH="/opt/env/bin:$PATH"

# Configurar PYTHONPATH
ENV PYTHONPATH=/usr/app/src/tienda_api

# Establecer el directorio de trabajo en el contenedor
WORKDIR /usr/app/src

# Copiar el archivo de requisitos y las dependencias
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de tu aplicación al contenedor
COPY tienda_api/ ./tienda_api/


# Exponer el puerto en el que tu aplicación se ejecutará
EXPOSE 8080

# Comando para ejecutar la aplicación FastAPI
CMD ["uvicorn", "tienda_api.main:app", "--host", "0.0.0.0", "--port", "8080"]