import streamlit as st
import requests
import sys
sys.path.append('/app')
from services.config import settings

st.title("🧠 Treinar Modelo")
# st.header("🧠 Treinar Modelo")

if st.button("Executar treinamento"):
    
    if "modo_teste" not in st.session_state:
        st.session_state["modo_teste"] = False
    
    if "endpoints" not in st.session_state:
        st.session_state["endpoints"] = (
            settings.ENDPOINTS_MOCK if st.session_state["modo_teste"] else settings.ENDPOINTS
        )

    # Usa o endpoint correto
    url = st.session_state["endpoints"]["TREINAMENTO"]
    try:
        # response = requests.post(TREINO_URL)
        # url = settings.ENDPOINTS["TREINAMENTO"]
        response = requests.post(url)
        if response.status_code == 200:
            # st.success("Modelo treinado com sucesso!")
            result = response.json()
            st.success(f"Resultado: {result['mensagem']}")
        else:
            st.error("Erro ao treinar modelo.")
            # result = response.json()
            # st.success(f"Resultado: {result['mensagem']}")
    except Exception as e:
        st.error(f"Erro de conexão com backend: {e}")
