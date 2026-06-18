import pandas as pd
from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL


def load_model() -> SentenceTransformer:
    """Charge le modèle d'embedding depuis le cache local."""
    return SentenceTransformer(EMBEDDING_MODEL)


def embed_chunks(df: pd.DataFrame, model: SentenceTransformer, batch_size: int = 32) -> pd.DataFrame:
    """Ajoute une colonne 'embedding' au DataFrame. Ne modifie pas l'original."""
    texts = df["text"].tolist()
    embeddings = model.encode(texts, batch_size=batch_size, show_progress_bar=True)
    result = df.copy()
    result["embedding"] = list(embeddings)
    return result
