# Serviço de Inferência - BestSeller Value Advisor

Este serviço realiza inferências utilizando um modelo de Machine Learning no formato TFLite, para prever o desempenho potencial de um livro como bestseller com base em diversos atributos fornecidos pelo usuário.

## 📖 Visão Geral

O serviço é desenvolvido em FastAPI e utiliza TensorFlow Lite Runtime para rodar o modelo otimizado em ambiente Docker.

---

## 🛠️ Tecnologias Utilizadas

- **FastAPI**
- **TensorFlow Lite Runtime**
- **Docker**
- **Python 3.9-slim**

---

## 📂 Estrutura do Diretório

```
services/backend/inference/
├── Dockerfile
├── requirements.txt
└── src/
    ├── inference.py
    └── model.tflite
```

---

## ⚙️ Como Executar

### Com Docker Compose

Certifique-se de estar na raiz do projeto e execute:

```bash
docker-compose up --build inference
```

### Individualmente com Docker

```bash
docker build -t bestseller/inference -f services/backend/inference/Dockerfile .
docker run -p 8003:8000 bestseller/inference
```

O serviço ficará disponível em: `http://localhost:8003`

---

## 🚀 Endpoint de Inferência

### **POST `/inference`**

Exemplo de payload:

```json
{
    "name": "Nome do Livro",
    "author": "Nome do Autor",
    "genre": "Fiction",
    "user_rating": 4.5,
    "reviews": 1500,
    "min_price": 20.0,
    "year": 3
}
```

**Resposta de sucesso:**

```json
{
    "mensagem": "Inferência realizada com sucesso",
    "resultado": 0.85
}
```

---

## 🔍 Debugging

Logs detalhados podem ser visualizados diretamente no container Docker ou no terminal:

```bash
docker-compose logs -f inference
```

---

## 📌 Dependências

Consulte o arquivo `requirements.txt` para verificar todas as dependências necessárias:

```bash
fastapi==0.95.1
uvicorn==0.22.0
tflite-runtime==2.14.0
numpy==1.23.0
```

---

## 📋 Licença

Este projeto é licenciado sob a licença MIT.

