from pydantic import BaseModel

class Formulario(BaseModel):
    Gender: str
    Age: str
    fav_music_genre: str
    music_time_slot: str
    music_Influencial_mood: str
    music_lis_frequency: str
