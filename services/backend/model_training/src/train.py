# services/backend/model_training/src/train.py

from fastapi import FastAPI, HTTPException
import pandas as pd
import numpy as np
import psycopg2
import os
from psycopg2.extras import DictCursor
from typing import Any
import joblib

# Para simplificar, vamos usar tf.keras diretamente aqui
import tensorflow as tf
# from tensorflow.keras import Sequential
# from tensorflow.keras.layers import Dense

# Import das configurações do projeto
from services.config import settings

# Import do modelo definido em autoencoder.py
from src.model.autoencoder import create_autoencoder

# Aqui supomos que exista (ou você pode criar) um módulo de conexão com BD.
# Caso não exista, vamos criar uma função inline para obter a conexão,
# similar ao que foi feito no ingest_data.py:
def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "postgres"),
        password=os.getenv("DB_PASS", "postgres"),
        dbname=os.getenv("DB_NAME", "best_sellers")
    )

app = FastAPI()

def check_numeric_issues(df: pd.DataFrame, columns_to_check: list[str]) -> None:
    """
    Percorre as colunas informadas e tenta converter cada valor para float.
    Caso encontre algo não numérico, imprime um aviso mostrando qual valor e em qual linha.

    :param df: DataFrame a ser verificado
    :param columns_to_check: Lista de nomes de colunas que deveriam ser numéricas
    """
    print(f"Verificando possíveis valores inválidos nas colunas: {columns_to_check}")
    for col in columns_to_check:
        if col not in df.columns:
            print(f"[AVISO] Coluna '{col}' não existe no DataFrame.")
            continue

        for idx, val in df[col].items():
            try:
                float(str(val).replace(',', '.'))  # tenta converter para float
            except ValueError:
                print(f"[ERRO] Coluna '{col}', linha {idx}: valor '{val}' não é numérico.")

def pre_process(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove colunas 'id', 'Name', 'Author' (se existirem),
    converte colunas numéricas para float/int,
    converte 'Year' e 'Genre' em categóricos.
    """
    print("Iniciando pré-processamento...")

    col_to_drop = ["Name", "Author"]
    if "id" in df.columns:
        col_to_drop.append("id")
    df = df.drop(columns=col_to_drop, errors="ignore")

    # Vamos primeiro garantir que as colunas numéricas não tenham valores não-numéricos
    numeric_cols = ["User Rating", "Reviews", "Price", "Year"]
    check_numeric_issues(df, numeric_cols)

    # Converte as colunas numéricas para float e depois int onde fizer sentido
    df["User Rating"] = df["User Rating"].astype(float)
    # Reviews, Price, Year como int, mas transformamos para float antes
    df["Reviews"] = df["Reviews"].astype(float).astype(int)
    df["Price"] = df["Price"].astype(float).astype(int)
    df["Year"] = df["Year"].astype(float).astype(int)

    # Transforma Year em categórico 0..10 (2009 -> 0, 2019 -> 10)
    df["Year"] = df["Year"].apply(lambda y: y - 2009)

    # Genre em categórico (0 = 'Non Fiction', 1 = 'Fiction')
    if "Genre" in df.columns:
        def genre_to_cat(g):
            if str(g).strip().lower() == "non fiction":
                return 0
            else:
                return 1
        df["Genre"] = df["Genre"].apply(genre_to_cat)

    return df
    
@app.post(settings.ENDPOINT_TREINAMENTO)
def treinar_modelo() -> Any:
    """
    Endpoint responsável por:
      1) Ler tabela de best_sellers do banco de dados.
      2) Pré-processar dados (remover colunas, transformar colunas em categórico, escalar).
      3) Treinar um modelo (ex. autoencoder) obtido de autoencoder.py.
      4) Mostrar perda nos dados best_sellers.
      5) Testar com not_best_sellers e mostrar perda.
      6) Calcular threshold e salvar em threshold_inference.py.
      7) Converter e salvar o modelo em formato TFLite e salvar também o scaler.
      8) Retornar resposta ao Streamlit indicando sucesso ou falha.
    """

    try:
        print("Iniciando o processo de treinamento...")

        # ---------------------------------------------------------------------
        # 1) Carregar dados do banco: best_sellers_csv (de settings)
        # ---------------------------------------------------------------------
        table_bestsellers = settings.TABLE_BEST_SELLERS
        print(f"Conectando ao banco de dados para ler tabela {table_bestsellers}...")
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=DictCursor)

        query_best = f"SELECT * FROM {table_bestsellers}"
        df_best = pd.read_sql(query_best, conn)
        print(f"Tabela {table_bestsellers} carregada. {len(df_best)} linhas.")
        
        # print("Colunas do dataframe:", df_best.columns)
        print("Head do dataframe:", df_best.head())

        # ---------------------------------------------------------------------
        # 2) Pré-processamento dos dados
        # ---------------------------------------------------------------------
        print("Iniciando pré-processamento...")

        df_best = pre_process(df_best)

        # Escalonamento (StandardScaler)
        from sklearn.preprocessing import StandardScaler
        print("Iniciando escalonamento (StandardScaler)...")
        scaler = StandardScaler()

        # Ajusta o scaler nos dados de best sellers
        X_train = scaler.fit_transform(df_best.values)

        # ---------------------------------------------------------------------
        # 3) Criar e treinar o modelo (usando autoencoder.py)
        # ---------------------------------------------------------------------
        print("Criando o modelo do autoencoder...")

        input_dim = X_train.shape[1]
        model = create_autoencoder(input_dim)

        print("Treinando o modelo (autoencoder)...")
        history = model.fit(
            X_train,                # Entrada
            X_train,                # Saída
            epochs=100,
            batch_size=16,
            validation_split=0.1,
            verbose=1,
            shuffle=True
        )

        print("Treinamento concluído.")
        
        # ---------------------------------------------------------------------        
        # 4) Mostrar perda nos dados best_sellers
        # ---------------------------------------------------------------------
        loss_best = model.evaluate(X_train, X_train, verbose=0)
        print(f"Perda do modelo nos dados 'best_sellers': {loss_best}")


        # ---------------------------------------------------------------------
        # 5) Testar o modelo com a tabela not_best_sellers_csv
        # ---------------------------------------------------------------------
        table_notbestsellers = settings.TABLE_NOT_BEST_SELLERS
        query_not_best = f"SELECT * FROM {table_notbestsellers}"
        print(f"Carregando e testando com a tabela {table_notbestsellers}...")
        df_not_best = pd.read_sql(query_not_best, conn)
        conn.close()

        if len(df_not_best) == 0:
            print(f"Tabela {table_notbestsellers} está vazia ou não existe.")
        else:
            df_not_best = pre_process(df_not_best)
            X_test = scaler.transform(df_not_best.values)
            # Calculando a perda
            loss_not_best = model.evaluate(X_test, X_test, verbose=0)
            print(f"Perda do modelo nos dados '{table_notbestsellers}': {loss_not_best}")

		# ---------------------------------------------------------------------
		# (6) Calcular um threshold e salvar em threshold_inference.py
		# ---------------------------------------------------------------------
        # Calcula reconstrução para cada item de X_train
        X_train_pred = model.predict(X_train)
        row_errors = np.mean((X_train_pred - X_train)**2, axis=1)

        # Define threshold como média + 2 desvios-padrão
        # threshold = np.mean(row_errors) + 2 * np.std(row_errors)
        threshold = ( loss_best + loss_not_best ) / 2
        print(f"Threshold calculado: {threshold}")

        # Salva no arquivo threshold_inference.py
        threshold_file_path = os.path.join(settings.TRAINED_MODELS_DIR, "threshold_inference.py")
        print(f"Salvando threshold em {threshold_file_path}...")
        with open(threshold_file_path, "w") as f:
            f.write(f"INFERENCE = {threshold:.4f}\n")  # 4 casas decimais


        # ---------------------------------------------------------------------
        # 7) Converter modelo para TFLite e salvar modelo + scaler
        # ---------------------------------------------------------------------
        print("Convertendo modelo para TFLite...")
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()

        # Diretório e nomes dos arquivos configurados em settings
        output_dir = settings.TRAINED_MODELS_DIR
        os.makedirs(output_dir, exist_ok=True)
        
        tflite_path = os.path.join(output_dir, settings.TFLITE_MODEL_FILENAME)
        scaler_path = os.path.join(output_dir, settings.SCALER_FILENAME)     

        with open(tflite_path, "wb") as f:
            f.write(tflite_model)
        print(f"Modelo TFLite salvo em {tflite_path}")

        # Salvando o scaler
        joblib.dump(scaler, scaler_path)
        print(f"Scaler salvo em {scaler_path}")

        # ---------------------------------------------------------------------
        # 6) Resposta final
        # ---------------------------------------------------------------------
        print("Treinamento finalizado com sucesso. Retornando resposta...")
        return {
            "mensagem": "Treinamento concluído com sucesso!",
            "modelo_tflite": tflite_path,
            "scaler": scaler_path,
            "threshold_file": threshold_file_path,
            "perda_best_sellers": float(loss_best),
            "perda_not_best_sellers": float(loss_not_best) if len(df_not_best) > 0 else None
        }

    except Exception as e:
        print(f"Erro durante o processo de treinamento: {e}")
        raise HTTPException(status_code=500, detail=str(e))
