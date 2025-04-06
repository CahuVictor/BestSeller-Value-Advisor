import streamlit as st
import requests
import sys
sys.path.append('/app')
from services.config import settings

st.title("🔍 Nova Inferência")
# st.header("📈 Nova Inferência")

# titulo = st.text_input("Título do Livro")
# autor = st.text_input("Autor")
# genero = st.selectbox("Gênero", ["Ficção", "Não Ficção"])
# rating = st.slider("Avaliação Média", 0.0, 5.0, 4.0, 0.1)
# reviews = st.number_input("Número de Resenhas", min_value=0)
# preco_min = st.number_input("Preço Mínimo", min_value=0.0)
# ano = st.slider("Anos no Futuro", 0, 10, 3)

with st.form("infer_form"):
    titulo = st.text_input("Título")
    autor = st.text_input("Autor")
    genero = st.selectbox("Gênero", ["Ficção", "Não Ficção"])
    rating = st.slider("Rating", 0.0, 5.0, 4.0)
    reviews = st.number_input("Resenhas", 0)
    preco_min = st.number_input("Preço mínimo", 1.0)
    ano = st.slider("Anos no futuro", 0, 10)

    enviado = st.form_submit_button("Enviar para inferência")

# if st.button("Analisar"):
if enviado:
    payload = {
        "titulo": titulo,
        "autor": autor,
        "genero": genero,
        "rating": rating,
        "reviews": reviews,
        "preco_min": preco_min,
        "ano": ano
    }
    url = st.session_state.get("url_base", "http://backend:8000") + "/inferir"
    try:
        response = requests.post(url, json=payload)
        result = response.json()
        st.success(f"Resultado: {result['mensagem']}")
    except Exception as e:
        st.error(f"Erro ao conectar com a API: {e}")
