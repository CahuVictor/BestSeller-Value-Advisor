import os

# -------------------------------------------------
# CONFIGURAÇÕES PARA Os ENDPOINTS
# -------------------------------------------------

# Hosts separados por ambiente
URL_MOCK = os.getenv("ENDPOINT_URL_MOCK", "http://mock-backend")
URL_INGEST = os.getenv("ENDPOINT_URL_INGEST", "http://data_ingestion")
URL_MODEL_TRAINING = os.getenv("ENDPOINT_URL_MODEL_TRAINING", "http://model_training")
URL_INFERENCE = os.getenv("ENDPOINT_URL_INFERENCE", "http://inference")

ENDPOINT_INFERENCIA = "/inference"
ENDPOINT_TREINAMENTO = "/model_training"
ENDPOINT_INGESTAO = "/data_ingestion"

PORT = os.getenv("ENDPOINT_PORT", "8000")
# PORT_MOCK = os.getenv("ENDPOINT_PORT_MOCK", "8000")
# PORT_INGEST = os.getenv("ENDPOINT_PORT_INGEST", "8001")

BASE_MOCK = f"{URL_MOCK}:{PORT}"
BASE_INGEST = f"{URL_INGEST}:{PORT}"
BASE_MODEL_TRAINING = f"{URL_MODEL_TRAINING}:{PORT}"
BASE_INFERENCE = f"{URL_INFERENCE}:{PORT}"

ENDPOINTS_MOCK = {
    "INFERENCIA": BASE_MOCK + os.getenv("ENDPOINT_INFERENCIA", ENDPOINT_INFERENCIA),
    "TREINAMENTO": BASE_MOCK + os.getenv("ENDPOINT_TREINAMENTO", ENDPOINT_TREINAMENTO),
    "INGESTAO": BASE_MOCK + os.getenv("ENDPOINT_INGESTAO", ENDPOINT_INGESTAO)
}

ENDPOINTS = {
    "INFERENCIA": BASE_INFERENCE + os.getenv("ENDPOINT_INFERENCIA", ENDPOINT_INFERENCIA),
    "TREINAMENTO": BASE_MODEL_TRAINING + os.getenv("ENDPOINT_TREINAMENTO", ENDPOINT_TREINAMENTO),
    "INGESTAO": BASE_INGEST + os.getenv("ENDPOINT_INGESTAO", ENDPOINT_INGESTAO)
}

# -------------------------------------------------
# CONFIGURAÇÕES PARA O FRONTEND
# -------------------------------------------------

# Ativa ou não o modo de exibição do botão de alternância de teste
SHOW_TEST_BUTTON = os.getenv("SHOW_TEST_BUTTON", "false").lower() == "true"

# -------------------------------------------------
# CONFIGURAÇÕES PARA O DATA INGESTION
# -------------------------------------------------

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

# -------------------------------------------------
# CONFIGURAÇÕES PARA O SERVIÇO DE TREINAMENTO
# -------------------------------------------------

# Tabelas que serão utilizadas no treinamento:
TABLE_BEST_SELLERS = CSV_TABLE_MAPPING[VALID_CSV_FILES[0]]
TABLE_NOT_BEST_SELLERS = CSV_TABLE_MAPPING[VALID_CSV_FILES[1]]

# Caminho (interno ao container) para salvar os artefatos do modelo
TRAINED_MODELS_DIR = "/services/trained_models"

# Nomes dos arquivos do modelo e scaler
TFLITE_MODEL_FILENAME = "model.tflite"
SCALER_FILENAME = "scaler.pkl"

# -------------------------------------------------
# CONFIGURAÇÕES PARA O SERVIÇO DE INFERÊNCIA
# -------------------------------------------------

# Número máximo de combinações geradas para inferência (ex.: 100)
MAX_COMBINATIONS = int(os.getenv("MAX_COMBINATIONS", 100))
# Multiplicador para definir o intervalo superior do preço (ex.: 3 vezes o preço mínimo)
PRICE_MULTIPLIER = int(os.getenv("PRICE_MULTIPLIER", 3))
# Número mínimo de combinações com erro abaixo do threshold para considerar o livro apto
MIN_SUCCESSFUL_COMBINATIONS = int(os.getenv("MIN_SUCCESSFUL_COMBINATIONS", 20))
