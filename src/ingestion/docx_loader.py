from docx import Document
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def load_docx(path: Path) -> dict:
    """Extrait le texte d'un fichier Word."""
    try:
        doc = Document(path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        full_text = "\n".join(paragraphs)
    except Exception as e:
        logger.warning(f"Impossible de lire {path}: {e}")
        return {"text": "", "source": str(path), "type": "docx", "skipped": True}

    if len(full_text.strip()) < 50:
        logger.warning(f"Ignoré {path}: texte trop court")
        return {"text": "", "source": str(path), "type": "docx", "skipped": True}

    return {"text": full_text, "source": str(path), "type": "docx", "skipped": False}


def load_docx_from_dir(directory: Path) -> list[dict]:
    """Charge tous les fichiers DOCX d'un répertoire (récursif)."""
    return [load_docx(p) for p in directory.glob("**/*.docx")]
