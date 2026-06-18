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


from src.pipeline.chunker import chunk_text, chunk_dataframe


def test_chunk_text_taille_correcte():
    """Chaque chunk (sauf le dernier) fait au plus chunk_size mots."""
    text = " ".join([f"mot{i}" for i in range(1200)])
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    for chunk in chunks[:-1]:
        assert len(chunk.split()) <= 500


def test_chunk_text_chevauchement():
    """Les 50 derniers mots d'un chunk sont les 50 premiers du suivant."""
    text = " ".join([f"mot{i}" for i in range(600)])
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) >= 2
    last_50_chunk0 = chunks[0].split()[-50:]
    first_50_chunk1 = chunks[1].split()[:50]
    assert last_50_chunk0 == first_50_chunk1


def test_chunk_text_texte_court_donne_un_seul_chunk():
    text = "mot " * 100
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) == 1


def test_chunk_dataframe_produit_chunk_ids_uniques():
    df = pd.DataFrame([
        {"text": "mot " * 600, "source": "a.pdf", "type": "pdf", "content_hash": "abc"}
    ])
    result = chunk_dataframe(df)
    assert "chunk_id" in result.columns
    assert result["chunk_id"].nunique() == len(result)


def test_chunk_dataframe_conserve_source_et_type():
    df = pd.DataFrame([
        {"text": "mot " * 600, "source": "cours.pdf", "type": "pdf", "content_hash": "abc"}
    ])
    result = chunk_dataframe(df)
    assert all(result["source"] == "cours.pdf")
    assert all(result["type"] == "pdf")
