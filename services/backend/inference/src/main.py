from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Livro(BaseModel):
    titulo: str
    autor: str
    genero: str
    rating: float
    reviews: int
    preco_min: float
    ano: int

@app.post("/inferir")
def inferir(livro: Livro):
    # Aqui você chamaria seu script de inferência com os dados recebidos
    return {"mensagem": "Livro tem potencial para best-seller! (simulação)"}
