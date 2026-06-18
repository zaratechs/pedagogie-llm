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


# --- docx_loader ---

def test_load_docx_valide_retourne_texte(tmp_path):
    """Un fichier DOCX valide retourne son texte."""
    from src.ingestion.docx_loader import load_docx

    fake_path = tmp_path / "cours.docx"
    fake_path.touch()

    mock_para1 = MagicMock()
    mock_para1.text = "Introduction à la pédagogie collégiale. " * 5
    mock_para2 = MagicMock()
    mock_para2.text = "Contenu du cours. " * 10
    mock_doc = MagicMock()
    mock_doc.paragraphs = [mock_para1, mock_para2]

    with patch("src.ingestion.docx_loader.Document", return_value=mock_doc):
        result = load_docx(fake_path)

    assert result["skipped"] is False
    assert "pédagogie" in result["text"]
    assert result["type"] == "docx"


def test_load_docx_trop_court_retourne_skipped(tmp_path):
    """Un DOCX avec trop peu de texte est marqué skipped."""
    from src.ingestion.docx_loader import load_docx

    fake_path = tmp_path / "vide.docx"
    fake_path.touch()

    mock_doc = MagicMock()
    mock_para = MagicMock()
    mock_para.text = "Court"
    mock_doc.paragraphs = [mock_para]

    with patch("src.ingestion.docx_loader.Document", return_value=mock_doc):
        result = load_docx(fake_path)

    assert result["skipped"] is True


# --- web_scraper ---

def test_scrape_url_valide_retourne_texte():
    """Une page web valide retourne son texte nettoyé."""
    from src.ingestion.web_scraper import scrape_url

    html = "<html><body><p>" + "contenu pédagogique " * 30 + "</p></body></html>"
    mock_response = MagicMock()
    mock_response.text = html
    mock_response.raise_for_status = MagicMock()

    with patch("src.ingestion.web_scraper.requests.get", return_value=mock_response):
        result = scrape_url("https://example.com")

    assert result["skipped"] is False
    assert "pédagogique" in result["text"]
    assert result["type"] == "web"
    assert result["source"] == "https://example.com"


def test_scrape_url_erreur_reseau_retourne_skipped():
    """Une erreur réseau retourne skipped sans planter."""
    from src.ingestion.web_scraper import scrape_url

    with patch("src.ingestion.web_scraper.requests.get", side_effect=Exception("timeout")):
        result = scrape_url("https://example.com")

    assert result["skipped"] is True
    assert result["text"] == ""


def test_scrape_url_sauvegarde_html(tmp_path):
    """Avec save_dir, le HTML brut est sauvegardé localement."""
    from src.ingestion.web_scraper import scrape_url

    html = "<html><body><p>" + "texte " * 30 + "</p></body></html>"
    mock_response = MagicMock()
    mock_response.text = html
    mock_response.raise_for_status = MagicMock()

    with patch("src.ingestion.web_scraper.requests.get", return_value=mock_response):
        scrape_url("https://example.com/page", save_dir=tmp_path)

    saved_files = list(tmp_path.glob("*.html"))
    assert len(saved_files) == 1
