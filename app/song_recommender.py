from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np

def get_song_from_db(track_id, songs_collection):
    """
    Obtiene la canción base desde la colección de canciones usando el track_id.
    """
    song = songs_collection.find_one({"track_id": track_id})
    if song:
        song["_id"] = str(song["_id"])  # Convertir ObjectId a string
    return song


def find_similar_songs_knn(base_song, songs_collection, feature_columns, n_songs, weight_SuperGenre=4, exclude_track_ids=None):
    """
    Encuentra canciones similares utilizando KNN con más peso para el género musical,
    evitando repeticiones y priorizando canciones del mismo artista.
    """
    songs_df = pd.DataFrame(list(songs_collection.find()))
    if songs_df.empty:
        return []

    # Excluir canciones ya recomendadas
    if exclude_track_ids:
        songs_df = songs_df[~songs_df["track_id"].isin(exclude_track_ids)]

    if songs_df.empty:
        return []

    # Validar campo "SuperGenre"
    songs_df["SuperGenre"] = songs_df["SuperGenre"].fillna("Unknown")
    songs_df["SuperGenre_encoded"] = songs_df["SuperGenre"].astype("category").cat.codes

    # Validar la canción base
    genre_categories = songs_df["SuperGenre"].astype("category").cat.categories
    if "SuperGenre" in base_song and base_song["SuperGenre"] in genre_categories:
        base_song["SuperGenre_encoded"] = genre_categories.get_loc(base_song["SuperGenre"])
    else:
        raise ValueError(f"La canción base no tiene un SuperGenre válido: {base_song.get('SuperGenre')}")

    feature_columns += ["SuperGenre_encoded"]

    # Normalización robusta
    songs_features = songs_df[feature_columns].fillna(0)
    songs_features_normalized = (songs_features - songs_features.mean()) / songs_features.std()

    # Aplicar peso al género musical
    genre_index = feature_columns.index("SuperGenre_encoded")
    songs_features_normalized.iloc[:, genre_index] *= weight_SuperGenre

    # Normalizar la canción base
    base_features = np.array([[base_song[col] if col in base_song else 0 for col in feature_columns]])
    base_features_normalized = (base_features - songs_features.mean().values) / songs_features.std().values
    base_features_normalized[:, genre_index] *= weight_SuperGenre

    # Entrenar KNN
    knn = NearestNeighbors(n_neighbors=min(n_songs * 2, len(songs_df)), metric="cosine")
    knn.fit(songs_features_normalized.values)

    # Encontrar canciones similares
    distances, indices = knn.kneighbors(base_features_normalized)
    similar_songs = songs_df.iloc[indices[0]]

    # Priorizar canciones del mismo artista
    same_artist_songs = similar_songs[similar_songs["artists"] == base_song["artists"]]
    remaining_songs = similar_songs[similar_songs["artists"] != base_song["artists"]]

    # Combinar priorizando canciones del mismo artista
    final_songs = pd.concat([same_artist_songs, remaining_songs]).head(n_songs)

    # Ordenar por popularidad y retornar
    return final_songs.sort_values(by=["popularity", "SuperGenre_encoded"], ascending=[False, True]).to_dict(orient="records")
