import json

FILE = "settings.json"

DEFAULT = {
    "snake_color": [0, 255, 0],
    "grid": True,
    "sound": True
}

def load_settings():
    try:
        with open(FILE, "r") as f:
            return json.load(f)
    except:
        return DEFAULT

def save_settings(data):
    with open(FILE, "w") as f:
        json.dump(data, f)