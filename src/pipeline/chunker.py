import pandas as pd
import hashlib
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    """Découpe un texte en chunks de chunk_size mots avec overlap mots de chevauchement."""
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        if len(chunk.strip()) > 50:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def chunk_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Explose chaque document en plusieurs lignes de chunks."""
    rows = []
    for _, row in df.iterrows():
        for i, chunk in enumerate(chunk_text(row["text"])):
            rows.append({
                "chunk_id": hashlib.sha256(chunk.encode()).hexdigest(),
                "text": chunk,
                "source": row["source"],
                "type": row["type"],
                "chunk_index": i,
            })
    return pd.DataFrame(rows)
