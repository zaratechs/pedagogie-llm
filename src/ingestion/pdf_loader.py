import pdfplumber
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def load_pdf(path: Path) -> dict:
    """Extrait le texte d'un PDF. Retourne un dict avec text, source, type, skipped."""
    try:
        with pdfplumber.open(path) as pdf:
            pages_text = [page.extract_text() or "" for page in pdf.pages]
    except Exception as e:
        logger.warning(f"Impossible de lire {path}: {e}")
        return {"text": "", "source": str(path), "type": "pdf", "skipped": True}

    full_text = "\n".join(pages_text)

    if len(full_text.strip()) < 50:
        logger.warning(f"Ignoré {path}: texte trop court ({len(full_text)} chars)")
        return {"text": "", "source": str(path), "type": "pdf", "skipped": True}

    return {"text": full_text, "source": str(path), "type": "pdf", "skipped": False}


def load_pdfs_from_dir(directory: Path) -> list[dict]:
    """Charge tous les PDFs d'un répertoire (récursif)."""
    return [load_pdf(p) for p in directory.glob("**/*.pdf")]
