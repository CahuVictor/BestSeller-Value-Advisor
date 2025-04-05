import streamlit as st
import requests
import sys
sys.path.append('/app')
from services.config import settings

st.title("🧠 Treinar Modelo")

if st.button("Executar treinamento"):
    url = st.session_state.get("url_base", "http://backend:8000") + "/treinar"
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
    except Exception as e:
        st.error(f"Erro de conexão com backend: {e}")
