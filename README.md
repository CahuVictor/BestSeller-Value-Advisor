# BestSeller Value Advisor

Este projeto utiliza Inteligência Artificial, especificamente um **autoencoder**, para recomendar o preço ideal e prever em quantos anos (de 0 até 10 anos) um livro tem potencial de se tornar best-seller, com base em padrões aprendidos de livros best-sellers da Amazon entre 2009 e 2019.

---

## Visão Geral

O projeto segue estas etapas principais:

O fluxo principal do projeto é:

1. **Treinamento do Autoencoder**: aprende padrões a partir do dataset de livros best-sellers (Amazon 2009–2019). O objetivo é capturar o “padrão” de livros que se destacaram no mercado.
2. **Validação**: verifica o desempenho com livros que não são best-sellers, confirmando que apresentam erro maior de reconstrução.
3. **Configuração**: para novos livros é definido um **preço mínimo**, um intervalo de possíveis preços (do preço mínimo até o preço máximo) e uma variação de “ano futuro” de 0 a **Ano Limite**, em que **0 = ano atual**, **1 = daqui a 1 ano** e assim por diante
4. **Otimização**: realiza até 100 testes ajustando preço (entre um valor mínimo e até 3 vezes este valor) e ano futuro (0 até 10 anos à frente).
5. **Avaliação**: se pelo menos "n" combinações tiverem um erro de reconstrução menor que o **threshold selecionado** (por exemplo a média observada nos best-sellers), o livro **tem potencial** de se tornar best-seller. Caso contrário, “descartamos” esse livro.

---

## Base de Dados

1. **Dataset Principal (Best-sellers)**  
   - Fonte: [Amazon Top 50 Bestselling Books 2009–2019](https://www.kaggle.com/datasets/sootersaalu/amazon-top-50-bestselling-books-2009-2019).  
   - Atributos Principais:  
     - Nome do Livro, Autor, Avaliação do Usuário (Rating), Número de Resenhas (Reviews), Preço, Ano(s) em que foi best-seller, Gênero (Ficção ou Não-ficção).  
   - Usado para **treinar** o autoencoder e extrair o **erro médio** de referência.

2. **Dataset Secundário (Não Best-sellers)**  
   - Conjunto criado ou obtido manualmente de livros que **não** atingiram status de best-seller.  
   - Serve para **validação**: esperamos que o autoencoder apresente erros de reconstrução maiores para livros sem o “padrão” de sucesso.

---

## Arquitetura Geral

### Coleta e Armazenamento
   - Datasets armazenados em banco de dados.
   - Pré-processamento dos dados (limpeza e normalização).
        - Remover dos dados de entrada título e autor
   - Definir o banco (MySQL, PostgreSQL etc.)
   - Ajustar parâmetros de conexão no arquivo de configuração (.env ou settings.py). 

### Treinamento e Validação
   - Treinamento do autoencoder com o dataset principal.
   - Validação com o dataset secundário.

#### Entradas
   - Recursos dos livros (preço, avaliação, número de reviews, etc.).
#### Saída
   - Reconstrução dos mesmos recursos.
#### Objetivo
   - Aprender o “espaço latente” que descreve um best-seller, minimizando o erro de reconstrução.
   - Após o treinamento, sabemos o erro médio de reconstrução do dataset de best-sellers.
   - Validação com Dataset de Não Best-sellers
   - Avaliamos o modelo no conjunto de livros que não tiveram sucesso.
   - Esperamos que o erro de reconstrução seja maior (em média), pois eles não seguem o “padrão” de um best-seller.


### Módulo de Otimização
   - Ajusta preço e ano futuro em testes iterativos.
   - Avalia combinações e identifica potencial de best-seller.

#### Entrada
   - livro “novo” (com certos atributos: título, autor, rating inicial, reviews, gênero (ficção ou não ficção))
   - Preço mínimo (entrada do usuário ou default)
   - Preço máximo (Opcional)
   - Intervalo de anos para teste (por exemplo, 2009 a 2025, ou 2009 a 2019, dependendo das regras do negócio) (Opcional)
#### Saída
   - Conjunto de y linhas da reconstrução da entrada
#### Objetivo
   - Gerar tabela de valores com n valores respeitando o intervalo
   - Fazer a combinação da tabela de valores com a tabela de anos para se tornar um bestseller (n valores x r intervalo de anos)
   - Filtrar tabela de valores x Ano para restar apenas y linhas para serem processadas  

### Módulo de Análise e Avaliação
   - Calcular o erro de reconstrução
   - Retornar se o livro tem potencial para ser um **best-seller**
   - Retornar o melhor resultado da combinação, a média dos 5 melhores resultados e gráficos do resultado.

#### Entrada
   - Conjunto de y linhas da reconstrução da entrada
#### Saída
   - Resultado e gráficos
#### Objetivo
   - Gerar tabela de valores com n valores respeitando o intervalo
   - Fazer a combinação da tabela de valores com a tabela de anos para se tornar um bestseller (n valores x r intervalo de anos)
   - Filtrar tabela de valores x Ano para restar apenas y linhas para serem processadas  


### Interface Web (Streamlit)
   - Permite inserir novos livros e preço mínimo.
   - Executa otimização e exibe análises e resultados.
   - Apresentar resultados
   - Permite inserir um novo livro (informações principais, preço mínimo etc.).
   - Executa o processo de iteração e retorna a “recomendação” (livro apto ou descartado).
   - Exibe também análises exploratórias (EDA) do dataset de best-sellers (distribuições de preços, anos, ratings, etc.).

#### Entrada
   - Novo livro
   - Valor mínimo
   - Valor máximo (Opcional)
   - Período de anos (Opcional)
#### Saída
   - Resultado do módulo de Análise e Avaliação apresentado na interface
#### Objetivo
   - Interação com o usuário
---

### Diagrama Simplificado

            [ Kaggle Best-sellers ]   [ Não Best-sellers ]       [ Novos Livros ]
                     |                        |                         |
                     | (import/load)          |                         |
                     v                        |                         v
              [Banco de Dados]     <---       +                    [Streamlit]  --->  (CRUD / Inserção de Novos Livros)
                     ^
                     | (treino/validação)
                     v
               [ Autoencoder Treinado ]
                     ^
                     | (nova entrada)
                     |  ( 100 tentativas de preço + ano futuro)
                     v
              [ Módulo de Otimização ]
                     ^
                     | (resultado do erro)
                     |
                [ Streamlit App ]
                     ^
                     | (usuário)
                     |
                  [Novo Livro]

```mermaid
graph TD
    Kaggle[Dataset Kaggle Best-sellers] --> BD[(Banco de Dados)]
    NãoBestSellers[Dataset Não Best-sellers] --> BD
    NovosLivros[Novos Livros] --> Streamlit
    BD --> Autoencoder[Autoencoder Treinado]
    Autoencoder --> Otimizacao[Módulo de Otimização]
    Streamlit --> Otimizacao
    Otimizacao --> StreamlitApp[Streamlit App]
    StreamlitApp --> Usuario[Usuário]
```

---

## Tecnologias Utilizadas

- **Python 3.x**  
- **Bibliotecas de Data Science / ML**:  
  - `pandas`, `numpy`, `scikit-learn` ou outra lib de Machine Learning.  
  - `tensorflow` ou `pytorch` (para o autoencoder).  
- **Streamlit** para interface web.  
- **Banco de Dados**: Pode ser **MySQL**, **PostgreSQL**, **MongoDB**, etc.  
- **Bibliotecas de visualização**: `matplotlib` (para gráficos).

---

## Estrutura de Diretórios

```
bestseller-value-advisor/
├── data/
│   ├── raw/                    	 # Dados originais
│   │   ├── best_sellers.csv         # Dataset Kaggle original
│   │   └── not_best_sellers.csv     # Dataset secundário
│   └── processed/                   # Dados pré-processados
│
├── notebooks/
│   ├── exploration.ipynb            # EDA e experimentos
│   └── autoencoder_training.ipynb   # Scripts de treinamento do autoencoder
│
├── models/                      	 # Modelos treinados
├── scaler/                			 # Scalers utilizados
├── schemas/                     	 # Schemas de validação e estrutura de dados
├── scripts/                   	     # Scripts auxiliares (limpeza, etc.)
│   └── data_cleaning.py        	 # Script de limpeza dos dados
│
├── src/
│   ├── app/                   	 	 # Aplicação Streamlit
│   │   └── streamlit_app.py         # Aplicação Streamlit
│   ├── db/
│   │   └── db_connection.py         # Conexão com BD
│   ├── model/
│   │   ├── autoencoder.py           # Definição do modelo
│   │   └── inference.py             # Rotina de inferência e otimização (preço/ano)
│   ├── settings.py                  # Configurações globais
│   └── utils/                       # Funções auxiliares│
├── docs/
│   └── README.md                    # Documentação adicional
│
├── docker-compose.yml               # Orquestração de containers
├── Dockerfile                       # Dockerfile da aplicação
├── pyproject.toml                   # Configuração do Poetry
├── poetry.lock
├── requirements.txt                 # Lista de dependências
└── README.md                        # Documentação principal (este arquivo)
```

---

## Guia de Instalação e Execução

### Clonar o Repositório
   ```bash
   git clone https://github.com/seu-usuario/bestseller-value-advisor.git
   cd bestseller-value-advisor

### Ambiente Virtual (Poetry) (Rodar local)
```bash
poetry install
poetry shell
```

---
## Execução com Docker

O projeto utiliza quatro containers Docker:

- **Container de Modelo**: cria, treina e analisa o modelo quando solicitado.
- **Container Streamlit**: aplicação frontend.
- **Container Banco de Dados**: armazenamento dos datasets.
- **Container Inferência**: realiza previsões e otimizações sob demanda.

Containers de inferência e treinamento são levantados sob demanda e desligados após execução.

### Levantar Containers

```bash
docker-compose up -d streamlit db
```

### Gerar Modelo (sob demanda)

```bash
docker-compose run --rm modelo
```

### Inferência (sob demanda)

```bash
docker-compose run --rm inferencia
```

---

### Fluxo Gerar Modelo Autoencoder

1. **Preprocessar os Dados**

Verifique se best_sellers.csv e not_best_sellers.csv estão em data/raw/.

2. **Executar a Aplicação (Streamlit)**

Inicializar docker-compose da aplicação
bash
Copiar
Editar
streamlit run src/app/streamlit_app.py

Acesse o endereço local (geralmente http://localhost:8501) e utilize a interface para inserir novos livros e verificar a recomendação.

3. **Preprocessar os Dados**

Execute scripts ou notebooks de limpeza e normalização, e armazene em data/processed/.

3. **Selecionar Gerar Modelo**

Ao selecionar a opção de gerar modelo, o fluxo irá Executar o notebook ou script responsável pelo treinamento (notebooks/autoencoder_training.ipynb ou src/model/autoencoder.py).

4. **Salvar Modelo**

Certificar-se de salvar o modelo treinado (por ex. model/best_seller_autoencoder.h5).

### Fluxo de Otimização (Preço + Ano Futuro)

Ao inserir um livro (fornecendo título, autor, rating etc.), o sistema:

Pede preço mínimo.

Gera até 100 combinações no intervalo [preço_mínimo, 3 × preço_mínimo] para preço e [0, 10] para “ano futuro”.

Calcula o erro de reconstrução em cada caso.

Se ≥ 20 dessas combinações tiverem erro abaixo do erro médio de reconstrução dos best-sellers, o livro é considerado “Apto a se tornar Best-seller”. Senão, “Descartado”.

---

## Próximos Passos
- Refinar a Métrica de Erro
- Decidir se o threshold será o erro médio + desvio padrão, mediana, ou se usaremos quartis.
- Ajustar hiperparâmetros do autoencoder para melhorar a distinção entre best-sellers e não best-sellers.
- Implementar Otimizações Mais Eficientes
- Ao invés de 100 tentativas aleatórias, poderemos usar algoritmos de busca ou heurísticas para encontrar o preço ótimo mais rapidamente.
- Adicionar Visualizações
- Criar gráficos no Streamlit para visualizar: distribuição dos preços, avaliações, número de reviews vs. erro de reconstrução.
- Tornar o Dataset Secundário Mais Rico
- Buscar ou criar mais exemplos de livros que não foram best-sellers, garantindo uma boa representatividade do mercado.
- Expandir dataset secundário.

---







## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
