from pathlib import Path
import re

import pymupdf

try:
    from docx import Document
except ImportError:  
    Document = None  


ALLOWED_EXTENSIONS = {".pdf", ".docx"}


def clean_extracted_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    cleaned_lines = []

    for line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", line).strip()

        if line:
            cleaned_lines.append(line)

    text = "\n".join(cleaned_lines)

    # Fix common PDF extraction cases where words become joined.
    text = re.sub(
        r"([a-z])([A-Z])",
        r"\1 \2",
        text,
    )

    # Normalize repeated whitespace again.
    text = re.sub(r"[ \t]+", " ", text)

    # Normalize excessive blank lines.
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF using PyMuPDF."""

    document = pymupdf.open(file_path)
    pages = []

    try:
        for page in document:
            page_text = page.get_text("text", sort=True)

            if page_text:
                pages.append(page_text)

    finally:
        document.close()

    raw_text = "\n".join(pages)

    return clean_extracted_text(raw_text)


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a DOCX file."""

    document = Document(file_path)
    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if text:
            paragraphs.append(text)

    raw_text = "\n".join(paragraphs)

    return clean_extracted_text(raw_text)


def extract_resume_text(file_path: str) -> str:
    """Extract text based on the resume file type."""

    extension = Path(file_path).suffix.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}. "
        "Only PDF and DOCX files are supported."
    )