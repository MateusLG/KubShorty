# Dockerfile

# 1. Imagem base: Python 3.11 slim
FROM python:3.11-slim

# 2. Define o diretório de trabalho dentro do container
WORKDIR /app

# 3. Atualiza o pip
RUN pip install --no-cache-dir pip --upgrade

# 4. Copia e instala as dependências PRIMEIRO
# (Isso aproveita o cache do Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copia o código da nossa aplicação (a pasta /app)
COPY ./app /app/app

# 6. Comando para rodar a aplicação
# - 'app.main:app' -> Encontre em /app/main.py o objeto 'app'
# - '--host 0.0.0.0' -> Aceite conexões de fora do container
# - '--reload' -> Reinicie o servidor automaticamente quando o código mudar (ÓTIMO para dev)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
