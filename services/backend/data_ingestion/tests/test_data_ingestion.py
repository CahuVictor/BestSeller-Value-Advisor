from fastapi.testclient import TestClient
from src.ingest_data import app

client = TestClient(app)

def test_ingest_data_csv():
    csv_content = """titulo,autor,genero,rating,reviews,preco_min,ano
Livro A,Autor A,Ficcao,4.5,100,19.99,2021
Livro B,Autor B,Drama,4.0,50,15.99,2020"""
    files = {"file": ("test.csv", csv_content, "text/csv")}
    response = client.post("/data_ingestion", files=files)
    assert response.status_code == 200
    assert response.json()["linhas_recebidas"] == 2

def test_ingest_data_not_csv():
    files = {"file": ("test.txt", "conteudo invalido", "text/plain")}
    response = client.post("/data_ingestion", files=files)
    assert response.status_code == 400
