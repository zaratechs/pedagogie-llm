import pandas as pd
import pytest
from src.pipeline.cleaner import clean_text, build_dataframe, save_skipped


def test_clean_text_supprime_lignes_vides_excessives():
    text = "Titre\n\n\n\nContenu du cours"
    result = clean_text(text)
    assert "\n\n\n" not in result


def test_clean_text_supprime_numeros_de_page():
    text = "Introduction\n\n42\n\nSuite du texte important"
    result = clean_text(text)
    lines = result.split("\n")
    assert not any(line.strip() == "42" for line in lines)


def test_clean_text_supprime_espaces_multiples():
    text = "mot    mot  mot"
    result = clean_text(text)
    assert "    " not in result


def test_build_dataframe_exclut_les_documents_skipped():
    docs = [
        {"text": "A " * 100, "source": "a.pdf", "type": "pdf", "skipped": False},
        {"text": "", "source": "b.pdf", "type": "pdf", "skipped": True},
    ]
    df = build_dataframe(docs)
    assert len(df) == 1
    assert "a.pdf" in df["source"].values


def test_build_dataframe_deduplique_le_contenu():
    same_text = "Contenu identique pédagogie. " * 30
    docs = [
        {"text": same_text, "source": "a.pdf", "type": "pdf", "skipped": False},
        {"text": same_text, "source": "b.pdf", "type": "pdf", "skipped": False},
    ]
    df = build_dataframe(docs)
    assert len(df) == 1


def test_build_dataframe_retient_les_colonnes_requises():
    docs = [{"text": "Texte valide. " * 20, "source": "a.pdf", "type": "pdf", "skipped": False}]
    df = build_dataframe(docs)
    for col in ["text", "source", "type", "content_hash"]:
        assert col in df.columns


def test_save_skipped_cree_csv(tmp_path):
    docs = [
        {"text": "", "source": "vide.pdf", "type": "pdf", "skipped": True},
        {"text": "long", "source": "ok.pdf", "type": "pdf", "skipped": False},
    ]
    save_skipped(docs, tmp_path)
    assert (tmp_path / "skipped.csv").exists()
    saved = pd.read_csv(tmp_path / "skipped.csv")
    assert len(saved) == 1
    assert "vide.pdf" in saved["source"].values
