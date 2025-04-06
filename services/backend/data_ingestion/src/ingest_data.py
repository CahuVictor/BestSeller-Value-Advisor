from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
import io
import sys
import os
import psycopg2
from psycopg2.extras import execute_values
from services.config import settings

app = FastAPI(
    title="Data Ingestion Service",
    description="Serviço responsável por ler CSV e inserir em uma base de dados.",
    version="1.0.0"
)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "postgres"),
        dbname=os.getenv("DB_NAME", "best_sellers")
    )

@app.post(settings.ENDPOINT_INGESTAO)
async def ingest_data(file: UploadFile = File(...)):
    if file.filename not in settings.VALID_CSV_FILES:
        raise HTTPException(status_code=400, detail=f"Arquivo '{file.filename}' não permitido. Apenas arquivos permitidos: {settings.VALID_CSV_FILES}")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="O arquivo enviado não é um CSV.")
    
    content = await file.read()
    try:
        # df = pd.read_csv(io.StringIO(content.decode("utf-8")), sep=",")
        df = pd.read_csv(io.StringIO(content.decode("utf-8")), sep=";")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler CSV: {e}")

    print(f"📥 CSV recebido com sucesso: CSV: {len(content)} bytes, linhas: {len(df)}")
    
    if df.empty:
        raise HTTPException(status_code=400, detail="CSV está vazio.")

    # Inserção no banco
    table_name = settings.CSV_TABLE_MAPPING[file.filename]

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        print("Conectado ao Banco de dados")

        # Cria a tabela se ela não existir
        print("Cria a tabela no banco de dados se ela não existir")
        columns = ", ".join([f'"{col}" TEXT' for col in df.columns])
        cur.execute(f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id SERIAL PRIMARY KEY,
                {columns}
            );
        """)
        
        print("Tabela criada com sucesso")
        
        # Inserção de dados
        print("Insere os dados no banco de dados")
        
        # # Inserção de dados
        # cols = [f'"{col}"' for col in df.columns]
        # insert_query = f'INSERT INTO not_best_sellers_csv ({", ".join(cols)}) VALUES %s'

        # # Conversão para lista de tuplas
        # from psycopg2.extras import execute_values
        # values = [tuple(row) for row in df.values]

        # Garante que todas as colunas estejam entre aspas duplas
        quoted_columns = ', '.join([f'"{col}"' for col in df.columns])

        for _, row in df.iterrows():
            values_placeholders = ','.join(['%s'] * len(row))
            cur.execute(
                f"INSERT INTO {table_name} ({quoted_columns}) VALUES ({values_placeholders})",
                tuple(row.astype(str))
            )
        print("Dados Inseridos com sucesso")

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        print(f"Erro ao inserir no banco de dados: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao inserir no banco de dados: {e}")

    # return {
    #     "mensagem": "CSV processado com sucesso.",
    #     "linhas_recebidas": len(df)
    # }
    
    print(f"📥 CSV processado com sucesso")
    return {
        "mensagem": "CSV processado e salvo com sucesso no banco de dados.",
        "linhas_inseridas": len(df)
    }
