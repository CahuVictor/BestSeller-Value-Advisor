import requests
import pandas as pd
import io

# docker build -t mock-backend .
# docker run -p 8000:8000 --name mock-backend-container --rm mock-backend
# docker rmi mock-backend

# Configurar as URLs dos serviços
INFERENCIA_URL = "http://localhost:8000/inferir"
TREINO_URL = "http://localhost:8001/treinar"
INGESTAO_URL = "http://localhost:8002/ingest"

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
    response = requests.post(INFERENCIA_URL, json=payload)
    assert response.status_code == 200
    print("✅ Inferência OK:", response.json())

def test_treino_modelo():
    response = requests.post(TREINO_URL)
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
    response = requests.post(INGESTAO_URL, files={"file": ("dados.csv", io.BytesIO(csv_bytes), "text/csv")})
    assert response.status_code == 200
    print("✅ Inserção CSV OK:", response.json())

if __name__ == "__main__":
    test_inferencia()
    test_treino_modelo()
    test_insercao_csv()
