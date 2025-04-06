import streamlit as st
import pandas as pd
import requests
import sys
sys.path.append('/app')
from services.config import settings

st.title("📥 Inserir CSV")

arquivo = st.file_uploader("Selecione um CSV", type="csv")
if arquivo:
    try:
        # Detectar codificação
        # raw_data = arquivo.read()
        # result = chardet.detect(raw_data)
        # encoding = result["encoding"]

        # Resetar ponteiro após leitura
        # arquivo.seek(0)

        # Tentar carregar com vírgula
        # df = pd.read_csv(arquivo, encoding=encoding)
        # df = pd.read_csv(arquivo)
        
        # Se só houver uma coluna, tentar ponto e vírgula
        # if len(df.columns) == 1:
            # arquivo.seek(0)
            # df = pd.read_csv(arquivo, sep=";", encoding=encoding)
            # df = pd.read_csv(arquivo, sep=";")
        
        arquivo.seek(0)
        df = pd.read_csv(arquivo, sep=";")
        
        st.dataframe(df.head())
        
    except Exception as e:
        st.error(f"Erro ao ler o CSV: {e}")
        st.stop()

    if df.empty or df.columns.size == 0:
        st.error("CSV vazio ou sem colunas.")
        st.stop()

    st.dataframe(df.head())

    if st.button("Enviar CSV para backend"):
        try:
            # response = requests.post(INGESTAO_URL, files={"file": arquivo})
            arquivo.seek(0)
            
            if "endpoints" not in st.session_state:
                st.session_state["endpoints"] = (
                    settings.ENDPOINTS_MOCK if st.session_state["modo_teste"] else settings.ENDPOINTS
                )

            # Usa o endpoint correto
            url = st.session_state["endpoints"]["INGESTAO"]
            
            response = requests.post(
                url,
                files={"file": (arquivo.name, arquivo, "text/csv")}
            )
            if response.status_code == 200:
                st.success("CSV inserido com sucesso!")
            else:
                st.error("Erro ao inserir CSV.")
        except Exception as e:
            st.error(f"Erro ao conectar com backend: {e}")
