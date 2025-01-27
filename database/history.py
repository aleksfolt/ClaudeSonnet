import json
import os


def save_chat_history(user_id, message, response):
    history_dir = "history"
    if not os.path.exists(history_dir):
        os.makedirs(history_dir)

    history_file = os.path.join(history_dir, f"{user_id}.json")

    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as file:
            history = json.load(file)
    else:
        history = []

    history.append({"user": message, "assistant": response})

    with open(history_file, "w", encoding="utf-8") as file:
        json.dump(history, file, ensure_ascii=False, indent=4)


def load_chat_history(user_id):
    history_file = os.path.join("history", f"{user_id}.json")

    if os.path.exists(history_file):
        with open(history_file, "r", encoding="utf-8") as file:
            return json.load(file)
    return []