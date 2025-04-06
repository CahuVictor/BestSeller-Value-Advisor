import streamlit as st
import sys
sys.path.append('/app')
from services.config import settings

st.set_page_config(page_title="BestSeller Value Advisor", layout="centered")

st.title("📘 BestSeller Value Advisor")

st.markdown("""
Bem-vindo! Este projeto utiliza um modelo de Autoencoder (IA) para avaliar o potencial de um livro se tornar um best-seller,
e recomendá-lo com base em combinações de preço e quantidade anos para se tornar um best-seller.

Use o menu à esquerda para:
- 🔍 Fazer uma inferência com novo livro
- 🧠 Treinar o modelo
- 📥 Inserir dados via CSV
""")

# Estado da sessão para o modo de teste
if "modo_teste" not in st.session_state:
    st.session_state["modo_teste"] = False

if "endpoints" not in st.session_state:
    st.session_state["endpoints"] = (
        settings.ENDPOINTS_MOCK if st.session_state["modo_teste"] else settings.ENDPOINTS
    )

# Exibir botão de ativar/desativar mock se a flag estiver habilitada
if settings.SHOW_TEST_BUTTON:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Ativar Modo Teste"):
            st.session_state["modo_teste"] = True
    with col2:
        if st.button("❌ Desativar Modo Teste"):
            st.session_state["modo_teste"] = False

# Mostra o modo atual
st.markdown(f"**Modo atual:** {'🧪 Teste (Mock)' if st.session_state['modo_teste'] else '🚀 Produção'}")

# Define os endpoints dinamicamente
if st.session_state["modo_teste"]:
    st.session_state["endpoints"] = settings.ENDPOINTS_MOCK
else:
    st.session_state["endpoints"] = settings.ENDPOINTS