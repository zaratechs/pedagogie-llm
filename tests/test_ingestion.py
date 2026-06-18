import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


# --- pdf_loader ---

def test_load_pdf_trop_court_retourne_skipped(tmp_path):
    """Un PDF dont le texte fait moins de 50 caractères est marqué skipped."""
    from src.ingestion.pdf_loader import load_pdf

    fake_path = tmp_path / "court.pdf"
    fake_path.touch()

    mock_pdf = MagicMock()
    mock_pdf.__enter__ = MagicMock(return_value=mock_pdf)
    mock_pdf.__exit__ = MagicMock(return_value=False)
    page = MagicMock()
    page.extract_text.return_value = "Court"
    mock_pdf.pages = [page]

    with patch("src.ingestion.pdf_loader.pdfplumber.open", return_value=mock_pdf):
        result = load_pdf(fake_path)

    assert result["skipped"] is True
    assert result["text"] == ""
    assert result["type"] == "pdf"


def test_load_pdf_valide_retourne_texte(tmp_path):
    """Un PDF avec assez de texte est retourné correctement."""
    from src.ingestion.pdf_loader import load_pdf

    fake_path = tmp_path / "valide.pdf"
    fake_path.touch()
    long_text = "mot pédagogique " * 60

    mock_pdf = MagicMock()
    mock_pdf.__enter__ = MagicMock(return_value=mock_pdf)
    mock_pdf.__exit__ = MagicMock(return_value=False)
    page = MagicMock()
    page.extract_text.return_value = long_text
    mock_pdf.pages = [page]

    with patch("src.ingestion.pdf_loader.pdfplumber.open", return_value=mock_pdf):
        result = load_pdf(fake_path)

    assert result["skipped"] is False
    assert "pédagogique" in result["text"]
    assert result["source"] == str(fake_path)
    assert result["type"] == "pdf"


def test_load_pdf_erreur_lecture_retourne_skipped(tmp_path):
    """Une erreur de lecture retourne skipped sans planter."""
    from src.ingestion.pdf_loader import load_pdf

    fake_path = tmp_path / "corrompu.pdf"
    fake_path.touch()

    with patch("src.ingestion.pdf_loader.pdfplumber.open", side_effect=Exception("fichier corrompu")):
        result = load_pdf(fake_path)

    assert result["skipped"] is True
