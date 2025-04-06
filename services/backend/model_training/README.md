# Serviço de Treinamento do Modelo - Model Training

Este serviço é parte do projeto **BestSeller Value Advisor** e é responsável por realizar o treinamento de um modelo de autoencoder para identificar características dos livros classificados como "Best Sellers". O modelo treinado é utilizado posteriormente em processos de inferência para prever se novos livros têm potencial de serem best sellers.

## Estrutura do Projeto

```
backend
├── model_training
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src
│       ├── train.py
│       ├── autoencoder.py
│       ├── settings.py
│       └── threshold_inference.py
└── trained_models
    ├── model.tflite
    ├── scaler.pkl
    └── threshold_inference.py
```

## Descrição dos Arquivos

- **Dockerfile:** Configura o ambiente Docker para execução do treinamento.
- **requirements.txt:** Lista as bibliotecas necessárias para o treinamento.
- **train.py:** Script principal que realiza o treinamento, pré-processamento de dados, validações, criação e treinamento do modelo, conversão para TFLite e cálculo do limiar (threshold).
- **autoencoder.py:** Contém a arquitetura do modelo autoencoder, dividida em encoder e decoder.
- **settings.py:** Arquivo que centraliza as configurações e caminhos utilizados pelo serviço.
- **threshold_inference.py:** Armazena o valor do threshold calculado após o treinamento.

## Como Funciona o Treinamento

1. **Conexão com o Banco de Dados:**
   - O serviço conecta-se a um banco PostgreSQL para obter dados das tabelas `best_sellers_csv` e `not_best_sellers_csv`.

2. **Pré-processamento dos Dados:**
   - Colunas desnecessárias são removidas (`Name`, `Author`, `id`).
   - Dados categóricos (`Year`, `Genre`) são convertidos em valores numéricos.
   - Dados são normalizados usando `StandardScaler`.

3. **Treinamento do Autoencoder:**
   - O modelo é treinado usando somente os dados da tabela de best sellers.
   - O modelo possui duas partes principais:
     - **Encoder:** Reduz os dados de entrada para uma dimensão latente (3 neurônios).
     - **Decoder:** Reconstrói os dados a partir da dimensão latente.

4. **Avaliação e Threshold:**
   - Após treinamento, é calculada a perda média nos dados best sellers e não best sellers.
   - O threshold de inferência é ajustado automaticamente baseado nesses valores e salvo para uso posterior.

5. **Conversão e Salvamento:**
   - O modelo treinado é convertido para o formato TFLite.
   - O scaler, o modelo e o valor do threshold são salvos na pasta `trained_models`.

## Execução com Docker

### Build da Imagem

```bash
docker build -t bestseller/model_training .
```

### Execução do Container

```bash
docker run -p 8002:8000 -v ./services/backend/trained_models:/services/trained_models bestseller/model_training
```

### Docker Compose

```yaml
model-training:
  build: ./services/backend/model_training
  container_name: bestseller-model-training-container
  ports:
    - 8002:8000
  volumes:
    - ./services/backend/trained_models:/services/trained_models
    - ./services/backend/model_training/src:/app/src
  networks:
    - bestseller-network
```

## Endpoints

- **`POST /model_training`:** Inicia o processo de treinamento completo do modelo.

## Logs e Monitoramento

O serviço exibe logs detalhados das etapas durante o treinamento, facilitando o acompanhamento e debug em tempo real.

---
