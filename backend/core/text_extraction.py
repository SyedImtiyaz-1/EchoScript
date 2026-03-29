import os
import fitz  # PyMuPDF
import docx
import pytesseract
from PIL import Image
from backend.config.settings import TESSERACT_CMD, TESSERACT_LANGS

pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def extract_from_text(text: str) -> str:
    return text.strip()


def extract_from_pdf(file_path: str) -> str:
    doc = fitz.open(file_path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    doc.close()
    return "\n".join(pages).strip()


def extract_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs).strip()


def extract_from_image(file_path: str) -> str:
    image = Image.open(file_path)
    langs = TESSERACT_LANGS.replace(",", "+")
    text = pytesseract.image_to_string(image, lang=langs)
    return text.strip()


EXTENSION_MAP = {
    ".pdf": extract_from_pdf,
    ".docx": extract_from_docx,
    ".doc": extract_from_docx,
    ".png": extract_from_image,
    ".jpg": extract_from_image,
    ".jpeg": extract_from_image,
    ".bmp": extract_from_image,
    ".tiff": extract_from_image,
    ".tif": extract_from_image,
    ".webp": extract_from_image,
    ".txt": lambda p: extract_from_text(open(p, encoding="utf-8").read()),
}


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[1].lower()
    extractor = EXTENSION_MAP.get(ext)
    if extractor is None:
        raise ValueError(f"Unsupported file type: {ext}")
    return extractor(file_path)
