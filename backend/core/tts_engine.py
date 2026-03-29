import re
import torch
from backend.config.settings import DEVICE, MAX_CHUNK_WORDS

_model = None


def get_model():
    global _model
    if _model is None:
        from chatterbox.mtl_tts import ChatterboxMultilingualTTS
        _model = ChatterboxMultilingualTTS.from_pretrained(device=DEVICE)
    return _model


def chunk_text(text: str, max_words: int = None) -> list[str]:
    if max_words is None:
        max_words = MAX_CHUNK_WORDS

    sentences = re.split(r'(?<=[.!?।。！？])\s+', text)
    chunks = []
    current_chunk = []
    current_words = 0

    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        word_count = len(sentence.split())

        if current_words + word_count > max_words and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = [sentence]
            current_words = word_count
        else:
            current_chunk.append(sentence)
            current_words += word_count

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    return chunks if chunks else [text]


def generate_speech(
    text: str,
    language_id: str,
    voice_path: str,
    exaggeration: float = 0.5,
    cfg_weight: float = 0.5,
) -> torch.Tensor:
    model = get_model()
    wav = model.generate(
        text,
        language_id=language_id,
        audio_prompt_path=voice_path,
        exaggeration=exaggeration,
        cfg_weight=cfg_weight,
    )
    return wav


def generate_long_speech(
    text: str,
    language_id: str,
    voice_path: str,
    exaggeration: float = 0.5,
    cfg_weight: float = 0.5,
) -> tuple[torch.Tensor, int]:
    model = get_model()
    sr = model.sr
    chunks = chunk_text(text)

    audio_parts = []
    silence = torch.zeros(1, int(sr * 0.3))

    for i, chunk in enumerate(chunks):
        wav = generate_speech(chunk, language_id, voice_path, exaggeration, cfg_weight)
        if wav.dim() == 1:
            wav = wav.unsqueeze(0)
        audio_parts.append(wav.cpu())
        if i < len(chunks) - 1:
            audio_parts.append(silence)

    final_wav = torch.cat(audio_parts, dim=1)
    return final_wav, sr
