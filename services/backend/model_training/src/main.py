from fastapi import FastAPI

app = FastAPI()

@app.post("/treinar")
def treinar_modelo():
    # Aqui você chamaria o script de treinamento
    # Ex: subprocess.run(["python", "train.py"])
    return {"mensagem": "Modelo treinado com sucesso! (simulação)"}
