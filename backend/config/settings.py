import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

# Device & Model
DEVICE = os.getenv("ECHOSCRIPT_DEVICE", "cuda")

# Tesseract OCR
TESSERACT_CMD = os.getenv("TESSERACT_CMD", "/usr/bin/tesseract")
TESSERACT_LANGS = os.getenv("TESSERACT_LANGS", "eng,hin,ara,fra,deu,spa,chi_sim,jpn,kor")

# Audio Output
OUTPUT_DIR = os.getenv("OUTPUT_DIR", os.path.join(os.path.dirname(__file__), "..", "output"))
MAX_OUTPUT_FILES = int(os.getenv("MAX_OUTPUT_FILES", "100"))

# Reference Voice Clips
MALE_VOICE_PATH = os.getenv("MALE_VOICE_PATH", os.path.join(os.path.dirname(__file__), "..", "assets", "voices", "male_reference.wav"))
FEMALE_VOICE_PATH = os.getenv("FEMALE_VOICE_PATH", os.path.join(os.path.dirname(__file__), "..", "assets", "voices", "female_reference.wav"))

# TTS Defaults
DEFAULT_CFG_WEIGHT = float(os.getenv("DEFAULT_CFG_WEIGHT", "0.5"))
DEFAULT_EXAGGERATION = float(os.getenv("DEFAULT_EXAGGERATION", "0.5"))
MAX_CHUNK_WORDS = int(os.getenv("MAX_CHUNK_WORDS", "400"))

# FastAPI Server
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))

# Emotion style presets: (exaggeration, cfg_weight)
EMOTION_PRESETS = {
    "neutral": (DEFAULT_EXAGGERATION, DEFAULT_CFG_WEIGHT),
    "expressive": (0.75, 0.3),
    "calm": (0.3, 0.6),
}

# Speed multipliers
SPEED_PRESETS = {
    "slow": 0.75,
    "normal": 1.0,
    "fast": 1.25,
}
