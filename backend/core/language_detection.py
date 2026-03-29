from langdetect import detect_langs
from backend.config.languages import SUPPORTED_LANGUAGES, normalize_lang_code


def detect_language(text: str) -> tuple[str, float]:
    results = detect_langs(text)
    if not results:
        return "en", 0.0

    top = results[0]
    code = normalize_lang_code(top.lang)
    if code is None:
        code = "en"
    return code, round(top.prob, 2)


def get_language_name(code: str) -> str:
    return SUPPORTED_LANGUAGES.get(code, code)
