import os

URL = os.getenv("ENDPOINT_URL", "http://mock-backend")
PORT = os.getenv("ENDPOINT_PORT", "8000")
BASE = f"{URL}:{PORT}"

ENDPOINTS = {
    "INFERENCIA": BASE + os.getenv("ENDPOINT_INFERENCIA", "/inferir"),
    "TREINAMENTO": BASE + os.getenv("ENDPOINT_TREINAMENTO", "/treinar"),
    "INGESTAO": BASE + os.getenv("ENDPOINT_INGESTAO", "/ingest")
}

# Ativa ou não o modo de exibição do botão de alternância de teste
SHOW_TEST_BUTTON = os.getenv("SHOW_TEST_BUTTON", "false").lower() == "true"