from fastapi import FastAPI, UploadFile, File
import pandas as pd

app = FastAPI()

@app.post("/ingest")
async def ingest_csv(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    # Aqui você inseriria os dados no banco
    print(df.head())  # apenas simulação
    return {"mensagem": "CSV recebido e processado! (simulação)"}
