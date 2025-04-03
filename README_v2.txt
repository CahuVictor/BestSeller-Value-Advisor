# BestSeller Value Advisor

Este projeto utiliza Inteligência Artificial, especificamente um **autoencoder**, para recomendar o preço ideal e prever em quantos anos (de 0 até 10 anos) um livro tem potencial de se tornar best-seller, com base em padrões aprendidos de livros best-sellers da Amazon entre 2009 e 2019.

---

## Visão Geral

O projeto é estruturado nas seguintes etapas principais:

### 1. Treinamento do Autoencoder
- **Objetivo:** Capturar padrões a partir dos livros best-sellers da Amazon (2009–2019).
- **Processo:** Treinamento utilizando características como preço, avaliação média, número de reviews e gênero (ficção ou não-ficção).

### 2. Validação
- **Objetivo:** Confirmar que o modelo diferencia claramente livros best-sellers dos não best-sellers.
- **Processo:** Avaliação do desempenho do autoencoder em um conjunto específico de livros não best-sellers, esperando um erro de reconstrução maior.

### 3. Configuração para Novos Livros
- **Objetivo:** Estabelecer parâmetros iniciais para avaliação de novos livros.
- **Entradas:** Preço mínimo definido pelo usuário, intervalo de preço (mínimo até 3x o mínimo), intervalo de anos futuros (0 = atual até 10 anos).

### 4. Otimização
- **Objetivo:** Identificar o melhor preço e ano futuro para maximizar potencial de best-seller.
- **Processo:** Realiza até 100 combinações de preços e anos, aplicando cada combinação ao modelo.

### 5. Avaliação dos Resultados
- **Objetivo:** Determinar o potencial de um novo livro se tornar best-seller.
- **Critério:** Se pelo menos "n" combinações tiverem erro inferior ao threshold (por exemplo, média dos erros dos best-sellers), o livro é considerado apto; caso contrário, é descartado.

---

## Execução com Docker

O projeto roda através de quatro containers Docker:

- **Container de Modelo:** Cria, treina e analisa o modelo (executado sob demanda).
- **Container Streamlit:** Fornece interface web para interação.
- **Container Banco de Dados:** Armazena datasets e resultados.
- **Container Inferência:** Executa previsões e otimizações (executado sob demanda).

Containers de inferência e treinamento são iniciados apenas quando necessários.

---

## Base de Dados

### Dataset Principal (Best-sellers)
- **Fonte:** [Amazon Top 50 Bestselling Books 2009–2019](https://www.kaggle.com/datasets/sootersaalu/amazon-top-50-bestselling-books-2009-2019).
- **Atributos:** Nome do Livro, Autor, Avaliação Média, Número de Reviews, Preço, Ano(s) como Best-seller, Gênero.

### Dataset Secundário (Não Best-sellers)
- **Fonte:** Criado manualmente ou obtido de fontes externas.
- **Objetivo:** Validação do modelo.

---

## Arquitetura Geral

### Coleta e Armazenamento
- Armazenamento em banco de dados (MySQL, PostgreSQL, etc.).
- Pré-processamento: limpeza, normalização e exclusão de atributos não relevantes (título, autor).
- Configuração feita via arquivo `.env` ou `settings.py`.

### Treinamento e Validação do Autoencoder
- **Entradas:** Características relevantes dos livros.
- **Saída:** Reconstrução das mesmas características.
- **Objetivo:** Reduzir o erro de reconstrução, identificando padrões latentes dos best-sellers.

### Módulo de Otimização
- Recebe informações do novo livro, preço mínimo e intervalos opcionais de preço máximo e anos futuros.
- Gera combinações e seleciona um subconjunto limitado para análise.

### Módulo de Análise e Avaliação
- Calcula o erro de reconstrução para cada combinação.
- Identifica as combinações com potencial real para best-seller.
- Retorna gráficos e métricas detalhadas dos resultados.

### Interface Web (Streamlit)
- Permite inserção de novos livros e parâmetros.
- Exibe resultados do módulo de análise e gráficos.
- Apresenta análises exploratórias do dataset principal.

---

### Diagrama Simplificado

```mermaid
graph TD
    Kaggle[Dataset Kaggle Best-sellers] --> BD[(Banco de Dados)]
    NãoBestSellers[Dataset Não Best-sellers] --> BD
    NovosLivros[Novos Livros] --> Streamlit
    BD --> Autoencoder[Autoencoder Treinado]
    Autoencoder --> Otimizacao[Módulo de Otimização]
    Streamlit --> Otimizacao
    Otimizacao --> Analise[Módulo de Análise e Avaliação]
    Analise --> StreamlitApp[Interface Streamlit]
    StreamlitApp --> Usuario[Usuário]
```

---

## Tecnologias Utilizadas

- Python 3.x  
- Pandas, NumPy, Scikit-Learn
- TensorFlow ou PyTorch
- Streamlit
- MySQL, PostgreSQL, MongoDB
- Matplotlib
- Docker

---

## Estrutura do Projeto

```
bestseller-value-advisor/
├── data/
│   ├── raw/                # Dados originais
│   └── processed/          # Dados pré-processados
│
├── notebooks/              # Notebooks de análise e treinamento
├── models/                 # Modelos treinados
├── scaler/                 # Scalers utilizados
├── schemas/                # Schemas de validação
├── scripts/
│   └── data_cleaning.py    # Script para limpeza de dados
│
├── src/
│   ├── app/                # Aplicação Streamlit
│   ├── db/                 # Conexões ao Banco de Dados
│   ├── model/              # Modelo e inferências
│   ├── settings.py         # Configurações
│   └── utils/              # Funções auxiliares
│
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── poetry.lock
├── requirements.txt
└── README.md
```

---

## Ambiente Virtual (Poetry)

```bash
poetry install
poetry shell
```

---

## Execução Docker

### Iniciar Containers Principais
```bash
docker-compose up -d streamlit db
```

### Executar Treinamento de Modelo (sob demanda)
```bash
docker-compose run --rm modelo
```

### Executar Inferência (sob demanda)
```bash
docker-compose run --rm inferencia
```

---

## Licença

Projeto licenciado sob a [MIT License](LICENSE).
