from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime
from app.database import get_database
from app.recommender import find_similar_profile_knn
from app.song_recommender import find_similar_songs_knn, get_song_from_db
from app.utils import serialize_mongo_document
import hashlib

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def show_form(request: Request):
    """
    Muestra el formulario principal.
    """
    return templates.TemplateResponse("Formulario.html", {"request": request})


@router.post("/recommend/", response_class=HTMLResponse)
async def recommend(
    request: Request,
    Gender: str = Form(...),
    Age: str = Form(...),
    fav_music_genre: str = Form(...),
    music_time_slot: str = Form(...),
    music_Influencial_mood: str = Form(...),
    music_lis_frequency: str = Form(...),
    Number_of_Songs: int = Form(...),
):
    """
    Genera una recomendación basada en los datos del formulario.
    """
    try:
        db = get_database()
        clusters_collection = db["Clusters"]
        songs_collection = db["canciones"]

        # Datos del usuario obtenidos del formulario
        user_data = {
            "Gender": Gender,
            "Age": Age,
            "fav_music_genre": fav_music_genre,
            "music_time_slot": music_time_slot,
            "music_Influencial_mood": music_Influencial_mood,
            "music_lis_frequency": music_lis_frequency,
        }

        # Encontrar perfiles similares
        similar_profiles = find_similar_profile_knn(
            user_data,
            clusters_collection,
            k=1,
            weight_music_lis_frequency=3,
            weight_fav_music_genre=11,
        )
        if not similar_profiles:
            raise HTTPException(status_code=404, detail="No se encontró un perfil similar.")

        # Obtener la canción base del perfil más similar
        profile = similar_profiles[0]
        base_song_id = profile.get("Track_ID")
        if not base_song_id:
            raise HTTPException(status_code=404, detail="El perfil no tiene una canción asignada.")

        base_song = get_song_from_db(base_song_id, songs_collection)
        if not base_song:
            raise HTTPException(status_code=404, detail="No se encontró la canción base.")

        # Seleccionar columnas de características para la recomendación
        feature_columns = [
            "danceability", "energy", "valence", "tempo", "loudness",
            "acousticness", "instrumentalness", "liveness", "popularity",
        ]

        # Encontrar canciones similares utilizando KNN
        similar_songs = find_similar_songs_knn(
            base_song,
            songs_collection,
            feature_columns,
            Number_of_Songs,
            weight_SuperGenre=4,  # Ajusta el peso del género
        )

        # Renderizar la plantilla resultados.html con los datos calculados
        return templates.TemplateResponse(
            "resultados.html",
            {
                "request": request,
                "user_data": user_data,
                "similar_profiles": similar_profiles,
                "assigned_song": base_song,
                "recommended_songs": similar_songs,
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
