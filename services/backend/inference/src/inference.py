from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
import os

# Alteração: Importar tflite_runtime ao invés de tensorflow
try:
    # import tflite_runtime.interpreter as tflite
    from tflite_runtime.interpreter import Interpreter
except ImportError:
    try:
        print("Erro import tflite_runtime.interpreter")
        from tensorflow.lite.python.interpreter import Interpreter
    except ImportError:
        print("Erro import tensorflow.lite.python.interpreter")
        raise ImportError("tflite_runtime e tensorflow.lite.python não está instalado. Verifique seu requirements.txt.")

import joblib

import io
import base64

# Configuração do matplotlib para ambientes sem display
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Importa as configurações globais
from services.config import settings

app = FastAPI()

# Função auxiliar para carregar o threshold salvo no treinamento.
def load_threshold() -> float:
    """
    Lê o arquivo threshold_inference.py e extrai o valor do erro médio de reconstrução (threshold)
    (espera que o arquivo contenha uma linha: INFERENCE = <valor>).
    """
    threshold_file = os.path.join(settings.TRAINED_MODELS_DIR, "threshold_inference.py")
    if not os.path.exists(threshold_file):
        raise Exception("Arquivo de threshold não encontrado.")
    with open(threshold_file, "r") as f:
        content = f.read().strip()
    try:
        # Supõe que o conteúdo seja: INFERENCE = <valor>
        value = float(content.split("=")[1].strip())
        return value
    except Exception as e:
        raise Exception("Erro ao carregar threshold: " + str(e))

# Modelo de entrada para o endpoint (dados vindos do frontend)
class BookInput(BaseModel):
    name: str           # Título do livro (para exibição, não utilizado no modelo)
    author: str         # Autor do livro (idem)
    user_rating: float  # Nota do usuário
    reviews: int        # Número de reviews
    genre: str          # Gênero ("Fiction" ou "Non Fiction")
    min_price: int      # Preço mínimo fornecido pelo usuário

# Função para converter o gênero em valor categórico (conforme definido no pré-processamento do treinamento)
def genre_to_cat(g: str) -> int:
    """
    Converte o gênero para categórico: 0 para "Non Fiction", 1 para "Fiction".
    """
    return 0 if g.strip().lower() == "non fiction" else 1

@app.post(settings.ENDPOINT_INFERENCIA)
def infer(book: BookInput):
    """
    Endpoint de inferência:
      1. Carrega o scaler e o modelo TFLite.
      2. Lê o threshold (erro médio dos best-sellers) salvo no treinamento.
      3. Gera combinações para os campos "Preço" (entre [min_price, 3×min_price]) e "Ano futuro" (entre 0 e 10),
         respeitando o número máximo de combinações configurado (ex.: 100).
         - Preço: intervalo [min_price, PRICE_MULTIPLIER × min_price]
         - Ano: intervalo [0, 10]
         O número máximo de combinações é definido por MAX_COMBINATIONS.
      4. Para cada combinação, forma o vetor de entrada (com os demais atributos constantes), escalona,
         realiza a inferência e calcula o erro de reconstrução (MSE).
      5. Calcula:
         - Quantas combinações possuem erro abaixo do threshold.
         - A média aritmética dos erros de todas as combinações.
         - A média ponderada de preço e ano para as combinações com erro abaixo do threshold,
           utilizando pesos que dão maior influência aos valores mais próximos de 0.
      6. Retorna também a melhor combinação (com menor erro) e uma visualização (histograma)
         dos erros de reconstrução.
      7. Retorna todos estes resultados, junto com os dados de entrada e a quantidade mínima de combinações bem-sucedidas.
    """
    try:
        print("Recebido dados do Frontend")
        
        # Caminhos dos artefatos
        scaler_path = os.path.join(settings.TRAINED_MODELS_DIR, settings.SCALER_FILENAME)
        tflite_model_path = os.path.join(settings.TRAINED_MODELS_DIR, settings.TFLITE_MODEL_FILENAME)
        
        # Verifica se os arquivos existem
        if not os.path.exists(scaler_path) or not os.path.exists(tflite_model_path):
            raise HTTPException(status_code=500, detail="Modelo TFLite ou scaler não encontrados.")

        # Carrega o scaler
        scaler = joblib.load(scaler_path)

        # Inicializa o interpretador do modelo TFLite
        # interpreter = tf.lite.Interpreter(model_path=tflite_model_path)
        interpreter = Interpreter(model_path=tflite_model_path)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()

        # Carrega o threshold (erro médio dos best-sellers) salvo no treinamento
        threshold = load_threshold()

        # Recupera as variáveis de configuração (com valores default se não estiverem definidos em settings.py)
        max_combinations = getattr(settings, "MAX_COMBINATIONS", 100)
        price_multiplier = getattr(settings, "PRICE_MULTIPLIER", 3)
        min_successful = getattr(settings, "MIN_SUCCESSFUL_COMBINATIONS", 20)

        # Determina as dimensões da grade (usando uma grade quadrada)
        n_grid = int(np.sqrt(max_combinations))
        if n_grid * n_grid < max_combinations:
            n_grid += 1  # Garante ao menos max_combinations combinações

        # Gera os valores para "Preço" e "Ano futuro"
        prices = np.linspace(book.min_price, price_multiplier * book.min_price, num=n_grid)
        # Para "Ano futuro", usamos 10 valores igualmente espaçados entre 0 e 10
        years = np.linspace(0, 10, num=n_grid)
        
        # Cria a grade de combinações
        price_grid, year_grid = np.meshgrid(prices, years)
        combinations = np.stack([price_grid.ravel(), year_grid.ravel()], axis=1)
        # Limita ao número máximo de combinações
        combinations = combinations[:max_combinations]

        # Prepara os demais atributos que permanecem constantes:
        # Vetor de features: [User Rating, Reviews, Preço, Ano Futuro, Gênero]
        genre_cat = genre_to_cat(book.genre)
        base_features = np.array([book.user_rating, book.reviews, 0, 0, genre_cat])
        
        # Monta os vetores de entrada para cada combinação gerada
        inputs = []
        for combo in combinations:
            price, year = combo
            vec = base_features.copy()
            vec[2] = price
            vec[3] = year  # O "Ano futuro" já está no intervalo 0 a 10
            inputs.append(vec)
        inputs = np.array(inputs)  # Shape: (max_combinations, 5)

        # Aplica o escalonamento
        inputs_scaled = scaler.transform(inputs)

        # Realiza a inferência em cada combinação e calcula o erro de reconstrução (MSE)
        errors = []
        for i in range(inputs_scaled.shape[0]):
            input_data = np.expand_dims(inputs_scaled[i], axis=0).astype(np.float32)
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            error = np.mean((input_data - output_data) ** 2)
            errors.append(error)
        errors = np.array(errors)

        # Conta quantas combinações tiveram erro abaixo do threshold
        # successful_count = int(np.sum(errors < threshold))
        successful_mask = errors < threshold
        successful_count = int(np.sum(successful_mask))

        # Determina o resultado conforme o número de combinações bem-sucedidas
        if successful_count >= min_successful:
            resultado = "Apto a se tornar Best-seller"
        else:
            resultado = "Descartado"
        
        # Calcula o erro médio aritmético de todas as combinações
        mean_error = float(np.mean(errors))

        # Cálculo da média ponderada para as combinações com erro abaixo do threshold
        successful_combinations = combinations[successful_mask]
        if successful_combinations.shape[0] > 0:
            # Para o ano, peso = (10 - ano + 1)
            weights_year = (10 - successful_combinations[:,1] + 1)
            # Para o preço, peso = (preço_max - preço + 1), onde preço_max = PRICE_MULTIPLIER * min_price
            price_max = price_multiplier * book.min_price
            weights_price = (price_max - successful_combinations[:,0] + 1)
            weighted_avg_year = float(np.sum(successful_combinations[:,1] * weights_year) / np.sum(weights_year))
            weighted_avg_price = float(np.sum(successful_combinations[:,0] * weights_price) / np.sum(weights_price))
        else:
            weighted_avg_year = None
            weighted_avg_price = None

        # Sugestão adicional: melhor combinação (menor erro)
        best_idx = int(np.argmin(errors))
        best_combination = {
            "price": float(combinations[best_idx, 0]),
            "year": float(combinations[best_idx, 1]),
            "error": float(errors[best_idx])
        }

        # Gera a visualização dos erros (histograma)
        fig, ax = plt.subplots()
        ax.hist(errors, bins=20, edgecolor="black")
        ax.set_title("Distribuição dos Erros de Reconstrução")
        ax.set_xlabel("Erro (MSE)")
        ax.set_ylabel("Frequência")
        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        buf.seek(0)
        error_histogram = base64.b64encode(buf.read()).decode("utf-8")
        plt.close(fig)

        # Retorna a resposta ao frontend
        return {
            "resultado": resultado,
            "sucessos": successful_count,
            "min_successful": min_successful,
            "total_combinacoes": int(len(errors)),
            "threshold": threshold,
            "mean_error": mean_error,
            "weighted_avg_price": weighted_avg_price,
            "weighted_avg_year": weighted_avg_year,
            "book_input": book.dict(),
            "best_combination": best_combination,
            "error_histogram": error_histogram,  # Imagem em base64 para visualização dos erros
            "errors": errors.tolist()  # Opcional: para debugging, pode remover em produção.
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
