import json
import random
from pathlib import Path

LEGENDS_DIR = Path("assets/legends")
LEGENDS_META_PATH = Path("legends/legends.json")

with LEGENDS_META_PATH.open(encoding="utf-8") as f:
    LEGENDS_DATA = json.load(f)

def get_all_legend_ids():
    return list(LEGENDS_DATA.keys())

def get_random_legend_id(exclude: set = None):
    ids = get_all_legend_ids()
    if exclude:
        ids = [i for i in ids if i not in exclude]
    if not ids:
        raise ValueError("Нет новых легенд.")
    return random.choice(ids)

def get_pdf_path(legend_id: str):
    return LEGENDS_DIR / f"{legend_id}.pdf"

def get_title(legend_id: str) -> str:
    return LEGENDS_DATA.get(legend_id, {}).get("title", "Без названия")

def get_description(legend_id: str) -> str:
    return LEGENDS_DATA.get(legend_id, {}).get("description", "")
