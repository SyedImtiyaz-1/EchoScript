SUPPORTED_LANGUAGES = {
    "ar": "Arabic",
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "fi": "Finnish",
    "fr": "French",
    "he": "Hebrew",
    "hi": "Hindi",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "ms": "Malay",
    "nl": "Dutch",
    "no": "Norwegian",
    "pl": "Polish",
    "pt": "Portuguese",
    "ru": "Russian",
    "sv": "Swedish",
    "sw": "Swahili",
    "tr": "Turkish",
    "zh": "Chinese",
}

# langdetect uses "zh-cn"/"zh-tw" for Chinese; map to Chatterbox "zh"
LANGDETECT_TO_CHATTERBOX = {
    "zh-cn": "zh",
    "zh-tw": "zh",
    "no": "no",
}


def normalize_lang_code(code: str) -> str | None:
    code = code.lower().strip()
    if code in SUPPORTED_LANGUAGES:
        return code
    return LANGDETECT_TO_CHATTERBOX.get(code)
