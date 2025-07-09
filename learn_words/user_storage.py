import json
from pathlib import Path

USER_DATA_FILE = Path("learn_words/user_data.json")


def load_users():
    if not USER_DATA_FILE.exists():
        return {}
    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_users(data: dict):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_user(user_id: int) -> dict:
    users = load_users()
    return users.get(str(user_id), {})


def update_user(user_id: int, updates: dict):
    users = load_users()
    uid = str(user_id)
    users[uid] = {**users.get(uid, {}), **updates}
    save_users(users)


def delete_user(user_id: int):
    users = load_users()
    users.pop(str(user_id), None)
    save_users(users)
