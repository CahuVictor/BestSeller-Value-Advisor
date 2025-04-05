# 📘 BestSeller Value Advisor - Frontend (Streamlit)

Este é o serviço de frontend da aplicação **BestSeller Value Advisor**, desenvolvido com **Streamlit**. Ele fornece uma interface amigável para analisar novos livros, treinar o modelo de autoencoder e inserir novos dados CSV no banco.

---

## 🔧 Funcionalidades

### ✅ Interface Interativa
- **Inserção de Novo Livro** para análise de potencial como best-seller.
- **Treinamento do Modelo** diretamente da interface.
- **Envio de Arquivos CSV** para ingestão de novos dados.

### 🔁 Alternância entre Ambientes (Produção vs Mock/Teste)
- Botões interativos para **ativar/desativar o modo de teste**.
- Controle via **variável de ambiente `SHOW_TEST_BUTTON`**.
- URLs de backend adaptadas automaticamente conforme o modo selecionado.
- Todas as páginas utilizam `st.session_state["url_base"]`.

---

## 🌍 Variáveis de Ambiente

Pode ser configurado via `.env` ou diretamente no `docker-compose.yml`:

```env
ENDPOINT_URL=http://backend
ENDPOINT_PORT=8000
ENDPOINT_INFERENCIA=/inferir
ENDPOINT_TREINAMENTO=/treinar
ENDPOINT_INGESTAO=/ingest
SHOW_TEST_BUTTON=true
```

---

## 🐳 Rodando com Docker Compose

Incluído um `docker-compose.yml` que sobe tanto o frontend quanto o mock-backend:

```bash
docker-compose up --build
```

---

## 🗂️ Estrutura

```
services/
└── frontend/
    ├── src/
    │   ├── streamlit_app.py         # Página principal com botão de alternância
    │   └── pages/
    │       ├── 1_Nova_Inferencia.py # Formulário e chamada de inferência
    │       ├── 2_Treinar_Modelo.py  # Botão para treinar modelo
    │       └── 3_Inserir_CSV.py     # Upload e envio de CSV para backend
    ├── Dockerfile
    ├── requirements.txt
    └── README.md (este arquivo)
```

---

## ✅ Requisitos

- Python 3.10+
- Docker e Docker Compose
- Dependências listadas em `requirements.txt`

---

## ✨ Exemplo de Comportamento

Na página inicial:

- Você verá um botão para **Ativar Modo Teste** e outro para **Desativar** (se `SHOW_TEST_BUTTON=true`).
- Dependendo do modo, a URL base dos requests mudará entre:
  - `http://backend:8000` (modo produção)
  - `http://mock-backend:8000` (modo teste)

---

## 📦 Build e Execução Manual

```bash
# Build manual
docker build -f services/frontend/Dockerfile -t streamlit:bestseller .

# Executar container
docker run -p 8501:8501 --name streamlit-container --env-file .env --rm streamlit:bestseller
```

---

## 🧪 Testes

Para testes automatizados da comunicação com os endpoints mockados, use o script `test_streamlit.py` com os containers ativos.

---

## 📃 Licença

MIT License.

---
---

docker rmi streamlit:bestseller
docker rm mock-backend-container streamlit-frontend
