import streamlit as st
import requests

st.header("📈 Nova Inferência")

titulo = st.text_input("Título do Livro")
autor = st.text_input("Autor")
genero = st.selectbox("Gênero", ["Ficção", "Não Ficção"])
rating = st.slider("Avaliação Média", 0.0, 5.0, 4.0, 0.1)
reviews = st.number_input("Número de Resenhas", min_value=0)
preco_min = st.number_input("Preço Mínimo", min_value=0.0)
ano = st.slider("Anos no Futuro", 0, 10, 3)

if st.button("Analisar"):
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
        st.success("Resultado:")
        st.json(response.json())
    except Exception as e:
        st.error(f"Erro de conexão com backend: {e}")
