FROM python:3.13-slim

# Variável de ambiente para logs não bufferizados
ENV PYTHONUNBUFFERED=1

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    gcc \
    python3-dev \
    pkg-config \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY . .

# Criar diretórios necessários
RUN mkdir -p /app/staticfiles /app/media

# Expor porta
EXPOSE 8000

# Comando padrão (será sobrescrito pelo docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "nextechlab.wsgi:application"]
