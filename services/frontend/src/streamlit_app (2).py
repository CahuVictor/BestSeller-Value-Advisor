import streamlit as st
from services.config import settings

st.set_page_config(page_title="BestSeller Value Advisor", layout="centered")
st.title("📘 BestSeller Value Advisor")

st.markdown("""
Este projeto utiliza um modelo de Autoencoder para avaliar o potencial de um livro se tornar um best-seller,
e recomendá-lo com base em combinações de preço e previsão de tempo.
""")

if "modo_teste" not in st.session_state:
    st.session_state["modo_teste"] = False

if settings.SHOW_TEST_BUTTON:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Ativar Modo Teste"):
            st.session_state["modo_teste"] = True
    with col2:
        if st.button("❌ Desativar Modo Teste"):
            st.session_state["modo_teste"] = False

st.markdown(f"**Modo atual:** {'🧪 Teste (Mock)' if st.session_state['modo_teste'] else '🚀 Produção'}")

st.session_state["url_base"] = "http://mock-backend:8000" if st.session_state["modo_teste"] else "http://backend:8000"
