import pytest
import numpy as np
import pandas as pd
from unittest.mock import MagicMock, patch


# --- vectorstore ---

def test_query_collection_retourne_chunks_formattes():
    """query_collection retourne une liste de dicts avec text, source, type, distance."""
    from src.rag.vectorstore import query_collection

    mock_collection = MagicMock()
    mock_collection.query.return_value = {
        "documents": [["Texte pédagogique pertinent."]],
        "metadatas": [[{"source": "cours.pdf", "type": "pdf"}]],
        "distances": [[0.12]],
    }

    result = query_collection(mock_collection, [0.1, 0.2, 0.3], top_k=1)

    assert len(result) == 1
    assert result[0]["text"] == "Texte pédagogique pertinent."
    assert result[0]["source"] == "cours.pdf"
    assert result[0]["type"] == "pdf"
    assert result[0]["distance"] == 0.12


def test_add_chunks_ignore_les_ids_existants():
    """add_chunks ne réinsère pas les chunks déjà présents dans ChromaDB."""
    from src.rag.vectorstore import add_chunks

    mock_collection = MagicMock()
    mock_collection.get.return_value = {"ids": ["id_existant"]}

    df = pd.DataFrame([
        {"chunk_id": "id_existant", "text": "texte", "source": "a.pdf", "type": "pdf",
         "embedding": np.array([0.1, 0.2])},
        {"chunk_id": "id_nouveau", "text": "nouveau texte", "source": "b.pdf", "type": "pdf",
         "embedding": np.array([0.3, 0.4])},
    ])

    added = add_chunks(mock_collection, df)

    assert added == 1
    call_kwargs = mock_collection.add.call_args.kwargs
    assert call_kwargs["ids"] == ["id_nouveau"]


def test_add_chunks_zero_si_tous_existants():
    """add_chunks retourne 0 si tous les chunks sont déjà indexés."""
    from src.rag.vectorstore import add_chunks

    mock_collection = MagicMock()
    mock_collection.get.return_value = {"ids": ["id1", "id2"]}

    df = pd.DataFrame([
        {"chunk_id": "id1", "text": "t1", "source": "a.pdf", "type": "pdf",
         "embedding": np.array([0.1])},
        {"chunk_id": "id2", "text": "t2", "source": "b.pdf", "type": "pdf",
         "embedding": np.array([0.2])},
    ])

    added = add_chunks(mock_collection, df)

    assert added == 0
    mock_collection.add.assert_not_called()
