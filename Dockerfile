FROM python:3.11-slim
#ENV PYTHONUNBUFFERED 1

WORKDIR /seguros

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./seguros/ ./

# Copiar el script de entrada y darle permisos de ejecución
COPY entrypoint.sh entrypoint.sh
RUN chmod +x entrypoint.sh

# Configurar el script de entrada como punto de entrada
ENTRYPOINT ["./entrypoint.sh"]
