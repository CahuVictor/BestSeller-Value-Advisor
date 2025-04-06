# FROM python:3.10-slim
FROM python:3.9-slim

WORKDIR /app

# Copiar o arquivo de requirements
COPY services/backend/model_training/requirements.txt /app/requirements.txt

# Instala as dependências
# RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia o código-fonte do serviço de treinamento
COPY services/backend/model_training/src /app/src

# Copia as configurações
COPY services/config/ services/config/

# Cria a pasta que receberá o modelo treinado (caso queira ter certeza que ela exista dentro do container)
RUN mkdir -p /services/trained_models

# Ajusta a variável de ambiente para que os imports funcionem
ENV PYTHONPATH=/app

# Expõe a porta do serviço de treino (caso você vá rodar um webserver)
EXPOSE 8000

# Comando padrão para rodar o FastAPI (ou outro framework) via uvicorn
CMD ["uvicorn", "src.train:app", "--host", "0.0.0.0", "--port", "8000"]