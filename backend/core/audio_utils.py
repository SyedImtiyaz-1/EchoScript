import os
import time
import uuid
import torch
import torchaudio
from pydub import AudioSegment
from backend.config.settings import OUTPUT_DIR, MAX_OUTPUT_FILES, SPEED_PRESETS, EMOTION_PRESETS


def get_emotion_params(style: str) -> tuple[float, float]:
    style = style.lower()
    return EMOTION_PRESETS.get(style, EMOTION_PRESETS["neutral"])


def get_speed_factor(speed: str) -> float:
    return SPEED_PRESETS.get(speed.lower(), 1.0)


def adjust_speed(wav: torch.Tensor, sample_rate: int, speed: str) -> tuple[torch.Tensor, int]:
    factor = get_speed_factor(speed)
    if factor == 1.0:
        return wav, sample_rate

    # Resample to simulate speed change while preserving pitch is complex;
    # simplest approach: change sample rate interpretation
    new_sr = int(sample_rate * factor)
    # Re-resample back to original sample rate to keep file format consistent
    wav = torchaudio.functional.resample(wav, orig_freq=new_sr, new_freq=sample_rate)
    return wav, sample_rate


def save_wav(wav: torch.Tensor, sample_rate: int, filename: str = None) -> str:
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if filename is None:
        filename = f"{uuid.uuid4().hex}.wav"
    path = os.path.join(OUTPUT_DIR, filename)
    if wav.dim() == 1:
        wav = wav.unsqueeze(0)
    torchaudio.save(path, wav, sample_rate)
    return path


def convert_to_mp3(wav_path: str) -> str:
    mp3_path = wav_path.rsplit(".", 1)[0] + ".mp3"
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3", bitrate="192k")
    return mp3_path


def cleanup_old_files(max_age_seconds: int = 3600):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    files = []
    for f in os.listdir(OUTPUT_DIR):
        if f.endswith((".wav", ".mp3")):
            fpath = os.path.join(OUTPUT_DIR, f)
            files.append((fpath, os.path.getmtime(fpath)))

    now = time.time()
    # Remove old files
    for fpath, mtime in files:
        if now - mtime > max_age_seconds:
            os.remove(fpath)

    # If still over limit, remove oldest
    remaining = sorted(
        [(f, m) for f, m in files if os.path.exists(f)],
        key=lambda x: x[1],
    )
    while len(remaining) > MAX_OUTPUT_FILES and remaining:
        os.remove(remaining.pop(0)[0])
