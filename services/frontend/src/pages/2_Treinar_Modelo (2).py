import streamlit as st
import requests

st.header("🧠 Treinar Modelo")

if st.button("Iniciar Treinamento"):
    url = st.session_state.get("url_base", "http://backend:8000") + "/treinar"
    try:
        response = requests.post(url)
        st.success("Resultado:")
        st.json(response.json())
    except Exception as e:
        st.error(f"Erro de conexão com backend: {e}")
