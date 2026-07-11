import json
from pathlib import Path

from .constants import MODEL_SAVE_FILE

try:
    from .constants import MODEL_SAVE_FILE
except ImportError:
    from constants import MODEL_SAVE_FILE

def load_channel_models():
    try:
        with open(MODEL_SAVE_FILE, encoding="utf-8") as f:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
    except FileNotFoundError:
        return {}

def save_channel_models(channel_models):
    with open(MODEL_SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(channel_models, f, ensure_ascii=False, indent=2)

channel_models = load_channel_models()