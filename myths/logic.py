import json
import os

MYTHS_FOLDER = "assets/myths"
DATA_PATH = "myths/myths.json"

def load_myths_data():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_myths_item(index: int):
    data = load_myths_data()
    if index < 0 or index >= len(data):
        return None
    return data[index]

def get_image_path(filename):
    return os.path.join(MYTHS_FOLDER, filename)

def total_items():
    return len(load_myths_data())