# FROM python:3.10-slim
FROM python:3.9-slim

WORKDIR /app

# Copiando os arquivos a partir da RAIZ do projeto
COPY services/backend/data_ingestion/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY services/backend/data_ingestion/src/ src/

COPY services/config/ services/config/

EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "src.ingest_data:app", "--host", "0.0.0.0", "--port", "8000"]
