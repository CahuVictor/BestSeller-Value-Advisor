from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import requests
import pandas as pd
import io
import sys
import os
sys.path.append('/app')
from services.config import settings_old

# docker build -t mock-backend .
# docker run -p 8000:8000 --name mock-backend-container --rm mock-backend
# docker rmi mock-backend

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
    print("🔍 Mock recebido: inferência")
    return {"mensagem": "Mock: livro recebido para inferência"}

@app.post("/treinar")
def treinar():
    print("🧠 Mock recebido: treinamento")
    return {"mensagem": "Mock: modelo treinado com sucesso"}

@app.post("/ingest")
async def ingest(file: UploadFile = File(...)):
    content = await file.read()
    print(f"📥 Mock recebido: CSV com {len(content)} bytes")
    return {"mensagem": "Mock: CSV processado com sucesso"}
