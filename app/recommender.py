from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np

def find_similar_profile_knn(user_data, clusters_collection, k=1, metric="cosine", weight_music_lis_frequency=3, weight_fav_music_genre=11):
    """
    Encuentra el perfil más parecido al usuario utilizando KNN, con pesos personalizados para Music_Frequency y Fav_Music_Genre.
    """
    clusters = list(clusters_collection.find({}, {"_id": 0}))
    clusters_df = pd.DataFrame(clusters)

    all_data = pd.concat([clusters_df, pd.DataFrame([user_data])], ignore_index=True)

    encoder = OneHotEncoder()
    encoded_data = encoder.fit_transform(
        all_data[["Gender", "Age", "fav_music_genre", "music_time_slot", "music_Influencial_mood", "music_lis_frequency"]]
    ).toarray()

    weights = np.ones(encoded_data.shape[1])

    # Pesos para 'music_lis_frequency'
    music_lis_frequency_categories = encoder.categories_[-1]
    music_lis_frequency_indices = np.arange(len(music_lis_frequency_categories)) + (encoded_data.shape[1] - len(music_lis_frequency_categories))
    weights[music_lis_frequency_indices] *= weight_music_lis_frequency

    # Pesos para 'fav_music_genre'
    fav_music_genre_categories = encoder.categories_[2]
    fav_music_genre_indices = np.arange(len(fav_music_genre_categories)) + (
        encoded_data.shape[1] - len(music_lis_frequency_categories) - len(fav_music_genre_categories)
    )
    weights[fav_music_genre_indices] *= weight_fav_music_genre

    weighted_data = encoded_data * weights

    user_vector = weighted_data[-1]
    existing_vectors = weighted_data[:-1]

    knn = NearestNeighbors(n_neighbors=k, metric=metric)
    knn.fit(existing_vectors)

    distances, indices = knn.kneighbors([user_vector])
    return clusters_df.iloc[indices[0]].to_dict(orient="records")
