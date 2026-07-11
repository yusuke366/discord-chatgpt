import json
from pathlib import Path

from .constants import PERSONA_FILES, PERSONA_SAVE_FILE

try:
    from .constants import PERSONA_FILES, PERSONA_SAVE_FILE
except ImportError:
    from constants import PERSONA_FILES, PERSONA_SAVE_FILE


def load_persona(filename: str) -> str:
    persona_dir = Path(__file__).resolve().parent / "personas"
    with (persona_dir / filename).open(encoding="utf-8") as f:
        return f.read()


def load_channel_personas():
    try:
        with open(PERSONA_SAVE_FILE, encoding="utf-8") as f:
            data = json.load(f)
            return {int(k): v for k, v in data.items()}
    except FileNotFoundError:
        return {}


def save_channel_personas(channel_personas):
    with open(PERSONA_SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(channel_personas, f, ensure_ascii=False, indent=2)


channel_personas = load_channel_personas()