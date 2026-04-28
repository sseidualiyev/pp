import json
import os

LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

# ── DEFAULTS ───────────────────────────────────────
DEFAULT_SETTINGS = {
    "sound": True,
    "difficulty": "normal"
}

DEFAULT_ENTRY = {
    "name": "Unknown",
    "score": 0,
    "distance": 0,
    "coins": 0
}


# ── GENERIC JSON HELPERS ───────────────────────────
def load_json(file, default):
    if not os.path.exists(file):
        return default
    try:
        with open(file, "r") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


# ── SETTINGS ───────────────────────────────────────
def load_settings():
    data = load_json(SETTINGS_FILE, {})
    
    # merge with defaults (important!)
    settings = DEFAULT_SETTINGS.copy()
    settings.update(data)

    return settings


def save_settings(settings):
    save_json(SETTINGS_FILE, settings)


# ── LEADERBOARD ────────────────────────────────────
def load_leaderboard():
    data = load_json(LEADERBOARD_FILE, [])

    fixed = []
    for e in data:
        entry = DEFAULT_ENTRY.copy()
        entry.update(e)  # fill missing keys like "coins"
        fixed.append(entry)

    return fixed


def save_leaderboard(entries):
    save_json(LEADERBOARD_FILE, entries)


def add_score(name, score, distance, coins):
    entries = load_leaderboard()

    # create safe entry
    entry = {
        "name": name,
        "score": int(score),
        "distance": int(distance),
        "coins": int(coins)
    }

    entries.append(entry)

    # sort by score (descending)
    entries.sort(key=lambda x: x["score"], reverse=True)

    # keep only top 10
    entries = entries[:10]

    save_leaderboard(entries)
    return entries