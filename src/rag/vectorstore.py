import chromadb
from pathlib import Path
import pandas as pd
from config.settings import VECTORDB_DIR


def get_collection(collection_name: str = "pedagogique") -> chromadb.Collection:
    """Ouvre ou crée la collection ChromaDB persistée sur disque."""
    client = chromadb.PersistentClient(path=str(VECTORDB_DIR))
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )


def add_chunks(collection: chromadb.Collection, df: pd.DataFrame) -> int:
    """Insère les chunks dans ChromaDB en ignorant les chunk_ids déjà présents."""
    existing_ids = set(collection.get()["ids"])
    new_rows = df[~df["chunk_id"].isin(existing_ids)]

    if new_rows.empty:
        return 0

    collection.add(
        ids=new_rows["chunk_id"].tolist(),
        documents=new_rows["text"].tolist(),
        embeddings=[e.tolist() for e in new_rows["embedding"]],
        metadatas=[
            {"source": row["source"], "type": row["type"]}
            for _, row in new_rows.iterrows()
        ],
    )
    return len(new_rows)


def query_collection(
    collection: chromadb.Collection,
    query_embedding: list[float],
    top_k: int = 5,
) -> list[dict]:
    """Retourne les top_k chunks les plus similaires à query_embedding."""
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {"text": doc, "source": meta["source"], "type": meta["type"], "distance": dist}
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        )
    ]
