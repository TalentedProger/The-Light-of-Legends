import os
import random
from pathlib import Path

import os
import json
import random
from pathlib import Path

IMAGES_DIR = Path("assets/images/proverbs_new")
PROVERBS_DB_PATH = Path("proverbs/proverbs.json")

# Загружаем пословицы в память один раз
with PROVERBS_DB_PATH.open(encoding="utf-8") as f:
    PROVERBS_DB = json.load(f)

def get_all_image_ids():
    return list(PROVERBS_DB.keys())

def get_random_image_id(exclude_list: set[str] = None) -> str:
    ids = get_all_image_ids()
    if exclude_list:
        ids = [i for i in ids if i not in exclude_list]
    if not ids:
        raise ValueError("Нет доступных пословиц")
    return random.choice(ids)


def get_image_path(image_id: str) -> Path:
    for ext in ['.jpg', '.png','.PNG']:
        path = IMAGES_DIR / f"{image_id}{ext}"
        if path.exists():
            return path
    raise FileNotFoundError(f"Image for ID {image_id} not found.")

def get_text_for_image(image_id: str) -> str:
    return PROVERBS_DB.get(image_id, "Пословица не найдена.")