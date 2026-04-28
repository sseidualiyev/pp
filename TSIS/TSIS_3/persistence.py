import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {
            "sound": True,
            "car_color": "blue",
            "difficulty": "normal"
        }
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)


