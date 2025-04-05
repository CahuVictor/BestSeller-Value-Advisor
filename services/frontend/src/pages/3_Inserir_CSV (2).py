import streamlit as st
import pandas as pd
import requests
import io

st.header("📤 Inserir CSV no Banco")

arquivo = st.file_uploader("Selecione um CSV", type="csv")

if arquivo:
    try:
        df = pd.read_csv(arquivo, sep=";")
        st.write("Pré-visualização dos dados:")
        st.dataframe(df.head())

        # Envio do arquivo ao backend
        arquivo.seek(0)
        files = {"file": ("dados.csv", arquivo, "text/csv")}
        url = st.session_state.get("url_base", "http://backend:8000") + "/ingest"
        response = requests.post(url, files=files)
        st.success("Resposta do Backend:")
        st.json(response.json())
    except Exception as e:
        st.error(f"Erro ao ler ou enviar o CSV: {e}")
