import os

# Hosts separados por ambiente
URL_MOCK = os.getenv("ENDPOINT_URL_MOCK", "http://mock-backend")
URL_INGEST = os.getenv("ENDPOINT_URL_INGEST", "http://data_ingestion")

ENDPOINT_INFERENCIA = "/inferir"
ENDPOINT_TREINAMENTO = "/treinar"
ENDPOINT_INGESTAO = "/data_ingestion"

PORT = os.getenv("ENDPOINT_PORT", "8000")
# PORT_MOCK = os.getenv("ENDPOINT_PORT_MOCK", "8000")
# PORT_INGEST = os.getenv("ENDPOINT_PORT_INGEST", "8001")

BASE_MOCK = f"{URL_MOCK}:{PORT}"
BASE_INGEST = f"{URL_INGEST}:{PORT}"

ENDPOINTS_MOCK = {
    "INFERENCIA": BASE_MOCK + os.getenv("ENDPOINT_INFERENCIA", ENDPOINT_INFERENCIA),
    "TREINAMENTO": BASE_MOCK + os.getenv("ENDPOINT_TREINAMENTO", ENDPOINT_TREINAMENTO),
    "INGESTAO": BASE_MOCK + os.getenv("ENDPOINT_INGESTAO", ENDPOINT_INGESTAO)
}

ENDPOINTS = {
    "INFERENCIA": BASE_MOCK + os.getenv("ENDPOINT_INFERENCIA", ENDPOINT_INFERENCIA),
    "TREINAMENTO": BASE_MOCK + os.getenv("ENDPOINT_TREINAMENTO", ENDPOINT_TREINAMENTO),
    "INGESTAO": BASE_INGEST + os.getenv("ENDPOINT_INGESTAO", ENDPOINT_INGESTAO)
}

# Ativa ou não o modo de exibição do botão de alternância de teste
SHOW_TEST_BUTTON = os.getenv("SHOW_TEST_BUTTON", "false").lower() == "true"

# Arquivos CSV válidos para upload
VALID_CSV_FILES = [
    "best_sellers.csv",
    "not_best_sellers.csv"
]

# Mapeamento de arquivos para nomes de tabela no banco de dados
CSV_TABLE_MAPPING = {
    "best_sellers.csv": "best_sellers_csv",
    "not_best_sellers.csv": "not_best_sellers_csv"
}