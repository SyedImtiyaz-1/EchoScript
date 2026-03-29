import os
import uuid
import shutil
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config.settings import OUTPUT_DIR, API_HOST, API_PORT
from backend.config.languages import SUPPORTED_LANGUAGES
from backend.core.text_extraction import extract_text, extract_from_text
from backend.core.language_detection import detect_language, get_language_name
from backend.core.tts_engine import generate_long_speech
from backend.core.audio_utils import (
    get_emotion_params,
    adjust_speed,
    save_wav,
    convert_to_mp3,
    cleanup_old_files,
)

app = FastAPI(title="EchoScript", description="AI-powered multilingual text-to-speech")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/languages")
def list_languages():
    return {"languages": SUPPORTED_LANGUAGES}


@app.post("/api/detect-language")
async def detect_lang(text: str = Form(...)):
    if not text.strip():
        raise HTTPException(400, "Text is empty")
    code, confidence = detect_language(text)
    return {
        "language_code": code,
        "language_name": get_language_name(code),
        "confidence": confidence,
    }


@app.post("/api/extract-text")
async def extract(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename or "")[1].lower()
    if not ext:
        raise HTTPException(400, "File has no extension")

    tmp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}{ext}")
    try:
        with open(tmp_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        text = extract_text(tmp_path)
        code, confidence = detect_language(text) if text.strip() else ("en", 0.0)
        return {
            "text": text,
            "language_code": code,
            "language_name": get_language_name(code),
            "confidence": confidence,
        }
    except ValueError as e:
        raise HTTPException(400, str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@app.post("/api/synthesize")
async def synthesize(
    text: str = Form(None),
    file: UploadFile = File(None),
    voice: str = Form("male"),
    language: str = Form("auto"),
    speed: str = Form("normal"),
    style: str = Form("neutral"),
):
    # 1. Get text
    if file is not None:
        ext = os.path.splitext(file.filename or "")[1].lower()
        tmp_path = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4().hex}{ext}")
        try:
            with open(tmp_path, "wb") as f:
                shutil.copyfileobj(file.file, f)
            final_text = extract_text(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    elif text:
        final_text = extract_from_text(text)
    else:
        raise HTTPException(400, "Provide either text or a file")

    if not final_text.strip():
        raise HTTPException(400, "No text could be extracted")

    # 2. Detect language
    if language == "auto":
        lang_code, _ = detect_language(final_text)
    else:
        lang_code = language

    if lang_code not in SUPPORTED_LANGUAGES:
        raise HTTPException(400, f"Unsupported language: {lang_code}")

    # 3. Resolve voice reference path
    from backend.config.settings import MALE_VOICE_PATH, FEMALE_VOICE_PATH
    voice_path = MALE_VOICE_PATH if voice.lower() == "male" else FEMALE_VOICE_PATH

    # 4. Get emotion params
    exaggeration, cfg_weight = get_emotion_params(style)

    # 5. Generate audio
    wav_tensor, sr = generate_long_speech(
        final_text, lang_code, voice_path, exaggeration, cfg_weight
    )

    # 6. Adjust speed
    wav_tensor, sr = adjust_speed(wav_tensor, sr, speed)

    # 7. Save WAV
    file_id = uuid.uuid4().hex
    wav_path = save_wav(wav_tensor, sr, f"{file_id}.wav")

    # 8. Convert to MP3
    mp3_path = convert_to_mp3(wav_path)

    # 9. Cleanup old files
    cleanup_old_files()

    return {
        "file_id": file_id,
        "language": lang_code,
        "language_name": get_language_name(lang_code),
        "wav_url": f"/api/download/{file_id}.wav",
        "mp3_url": f"/api/download/{file_id}.mp3",
    }


@app.get("/api/download/{filename}")
async def download(filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(path):
        raise HTTPException(404, "File not found")
    media_type = "audio/wav" if filename.endswith(".wav") else "audio/mpeg"
    return FileResponse(path, media_type=media_type, filename=filename)


if __name__ == "__main__":
    import uvicorn
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    uvicorn.run("backend.main:app", host=API_HOST, port=API_PORT, reload=True)
