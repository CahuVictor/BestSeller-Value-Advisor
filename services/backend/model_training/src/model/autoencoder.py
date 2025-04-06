import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense

def create_autoencoder(input_dim: int):
    """
    Cria e retorna um modelo Autoencoder simples com base no input_dim fornecido.

    :param input_dim: Dimensão de entrada dos dados
    :return: Instância de um modelo Keras (Autoencoder)
    """
    model = Sequential([
        # Encoder: comprime a entrada de 5 para 3 neurônios
        Dense(units=3, activation='relu', input_shape=(input_dim,)),
        
        # Decoder: reconstrói a saída para 5 neurônios
        # Na saída, usamos 'linear' (ou 'sigmoid', dependendo do caso)
        Dense(units=input_dim, activation='linear')
    ])
    
    model.compile(optimizer='adam', loss='mse')
    
    model.summary()
    
    return model
