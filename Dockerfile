# Dockerfile para o Resumidor de Vídeos do YouTube

FROM python:3.11-slim

# Metadados
LABEL maintainer="John <contato@projeto.com>"
LABEL description="Resumidor Inteligente de Vídeos do YouTube"
LABEL version="1.0.0"

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar arquivos de dependências
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar código da aplicação
COPY main.py .
COPY .env.example .env

# Criar usuário não-root
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Criar diretório para arquivos temporários
RUN mkdir -p /app/temp

# Expor porta
EXPOSE 8000

# Comando de saúde
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Comando padrão
CMD ["python", "main.py"]
