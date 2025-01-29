from pymongo import MongoClient

# Conexión con MongoDB
def get_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["music"]  # Nombre de tu base de datos
    return db

# app/config.py

# Configuración para el algoritmo de recomendación
RECOMMENDER_CONFIG = {
    "k": 1,                     # Número de vecinos a buscar
    "metric": "cosine",         # Métrica de distancia ('cosine', 'euclidean', etc.)
    "reduce_dim": True,         # Activar reducción de dimensionalidad
    "n_components": 10          # Número de componentes principales para PCA
}
