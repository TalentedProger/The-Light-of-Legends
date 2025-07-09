import os
import json
import random

import os
import random
import json

SONGS_FOLDER = "assets/songs"
DESCRIPTION_PATH = "songs/song_data.json"

def get_all_songs():
    return [f for f in os.listdir(SONGS_FOLDER) if f.endswith(".mp3")]

def get_song_path(filename):
    return os.path.join(SONGS_FOLDER, filename)

def get_song_description(filename):
    with open(DESCRIPTION_PATH, "r", encoding="utf-8") as f:
        descriptions = json.load(f)
    return descriptions.get(filename, "Описание отсутствует.")

def get_random_song(exclude: set):
    available = list(set(get_all_songs()) - exclude)
    if not available:
        raise ValueError("Все песни просмотрены.")
    return random.choice(available)
