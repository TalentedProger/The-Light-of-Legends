import json
import os

GALLERY_FOLDER = "assets/galery_pic"
DATA_PATH = "galery/gallery.json"

def load_gallery_data():
    with open(DATA_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_gallery_item(index: int):
    data = load_gallery_data()
    if index < 0 or index >= len(data):
        return None
    return data[index]

def get_image_path(filename):
    return os.path.join(GALLERY_FOLDER, filename)

def total_items():
    return len(load_gallery_data())
