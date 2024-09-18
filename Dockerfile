###########
# BUILDER #
###########

# Usar imagen base oficial de Python para la fase de construcción
FROM python:3.12-slim as builder

# Definir el directorio de trabajo
ENV APP_HOME=/seguros/seguros
WORKDIR $APP_HOME

# Instalar dependencias del sistema necesarias para la construcción
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    libmagic1 \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Actualizar pip e instalar las dependencias de Python
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /wheels -r requirements.txt

#########
# FINAL #
#########

# Usar la misma imagen base para la fase final
FROM python:3.12-slim

# Definir directorio de trabajo
ENV APP_HOME=/seguros/seguros
WORKDIR $APP_HOME

# Instalar cron y copiar las dependencias desde el builder
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libmagic1 \
    cron \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
COPY --from=builder $APP_HOME/requirements.txt .
RUN pip install --no-cache /wheels/*

# Copiar los archivos restantes de la aplicación
COPY ./seguros/ ./
COPY cronseguros.cfg cronseguros.cfg

# Copiar el script de entrada y darle permisos de ejecución
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# Configurar el script de entrada como punto de entrada
ENTRYPOINT ["bash", "entrypoint.sh"]
