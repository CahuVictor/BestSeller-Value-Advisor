# 📥 Data Ingestion Service

Este serviço faz parte do projeto **BestSeller Value Advisor** e é responsável por **receber arquivos CSV** contendo dados de livros e **inserir essas informações no banco de dados PostgreSQL**.

## 🚀 Funcionalidades

- Upload de arquivos `.csv` através de uma API FastAPI.
- Validação de nome e formato do arquivo.
- Leitura e parsing do CSV com Pandas.
- Criação automática da tabela no banco de dados, caso não exista.
- Inserção dos dados no PostgreSQL com `psycopg2`.

## 📁 Estrutura esperada de arquivos

Somente dois arquivos são permitidos para upload:

| Nome do Arquivo       | Nome da Tabela no Banco de Dados   |
|-----------------------|-------------------------------------|
| `best_sellers.csv`    | `best_sellers_csv`                  |
| `not_best_sellers.csv`| `not_best_sellers_csv`              |

Essas definições estão no arquivo `settings.py`.

## 🧱 Requisitos

- Docker + Docker Compose
- Python 3.9 (em ambiente dockerizado)
- Banco de dados PostgreSQL (configurado via Docker Compose)

## ⚙️ Configuração

### Variáveis de ambiente utilizadas

```env
DB_HOST=db
DB_PORT=5432
DB_USER=postgres
DB_PASS=postgres
DB_NAME=best_sellers
```

Essas variáveis são utilizadas para conectar com o banco de dados PostgreSQL.

## 🐳 Como rodar com Docker

1. Suba os containers:
   ```bash
   docker-compose up --build
   ```

2. Acesse a documentação interativa da API:
   - [http://localhost:8001/docs](http://localhost:8001/docs)

## 🔄 Endpoint de Upload

**POST** `/data_ingestion`

- **Parâmetro:** `file` (form-data, tipo: arquivo `.csv`)
- **Validações:**
  - Apenas arquivos `.csv`
  - Nome do arquivo deve ser `best_sellers.csv` ou `not_best_sellers.csv`
- **Retorno de sucesso:**
  ```json
  {
    "mensagem": "CSV processado e salvo com sucesso no banco de dados.",
    "linhas_inseridas": 600
  }
  ```

## 🧠 Exemplo de uso com `curl`

```bash
curl -X POST http://localhost:8001/data_ingestion   -F "file=@/caminho/para/best_sellers.csv"
```

## 🧼 Limpeza e reconstrução

Para resetar os containers e reconstruir do zero:
```bash
docker-compose down -v
docker-compose up --build
```
