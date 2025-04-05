import requests
import pandas as pd
import io
import sys
import os

# Permitir importar settings.py da pasta config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../config")))
from settings import ENDPOINTS

def test_inferencia():
    payload = {
        "titulo": "Livro Teste",
        "autor": "Autor X",
        "genero": "Ficção",
        "rating": 4.5,
        "reviews": 100,
        "preco_min": 19.99,
        "ano": 3
    }
    response = requests.post(ENDPOINTS["INFERENCIA"], json=payload)
    assert response.status_code == 200
    print("✅ Inferência OK:", response.json())

def test_treino_modelo():
    response = requests.post(ENDPOINTS["TREINAMENTO"])
    assert response.status_code == 200
    print("✅ Treinamento OK:", response.json())

def test_insercao_csv():
    df = pd.DataFrame([{
        "Name": "Teste",
        "Author": "Autor X",
        "User Rating": 4.3,
        "Reviews": 875,
        "Price": 22,
        "Year": 2020,
        "Genre": "Fiction"
    }])
    csv_bytes = df.to_csv(index=False).encode()
    response = requests.post(ENDPOINTS["INGESTAO"], files={"file": ("dados.csv", io.BytesIO(csv_bytes), "text/csv")})
    assert response.status_code == 200
    print("✅ Inserção CSV OK:", response.json())

if __name__ == "__main__":
    test_inferencia()
    test_treino_modelo()
    test_insercao_csv()
