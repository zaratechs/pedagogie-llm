"""Construit l'index ChromaDB depuis tous les documents dans data/raw/.

Usage :
    python scripts/build_index.py

Relancer après chaque ajout de nouveaux documents.
"""
import logging
from config.settings import RAW_DIR, PROCESSED_DIR, ERRORS_DIR
from src.ingestion.pdf_loader import load_pdfs_from_dir
from src.ingestion.docx_loader import load_docx_from_dir
from src.pipeline.cleaner import build_dataframe, save_skipped
from src.pipeline.chunker import chunk_dataframe
from src.pipeline.embedder import load_model, embed_chunks
from src.rag.vectorstore import get_collection, add_chunks

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    logger.info("Étape 1/5 : Ingestion des documents...")
    documents = []
    documents.extend(load_pdfs_from_dir(RAW_DIR))
    documents.extend(load_docx_from_dir(RAW_DIR))
    logger.info(f"  {len(documents)} documents chargés")

    save_skipped(documents, ERRORS_DIR)

    logger.info("Étape 2/5 : Nettoyage et déduplication...")
    df_clean = build_dataframe(documents)
    logger.info(f"  {len(df_clean)} documents valides après nettoyage")

    logger.info("Étape 3/5 : Découpage en chunks...")
    df_chunks = chunk_dataframe(df_clean)
    df_chunks.drop(columns=["chunk_index"]).to_parquet(
        PROCESSED_DIR / "chunks.parquet", index=False
    )
    logger.info(f"  {len(df_chunks)} chunks produits")

    logger.info("Étape 4/5 : Vectorisation...")
    model = load_model()
    df_embedded = embed_chunks(df_chunks, model)

    logger.info("Étape 5/5 : Indexation ChromaDB...")
    collection = get_collection()
    added = add_chunks(collection, df_embedded)
    logger.info(f"  {added} nouveaux chunks indexés")

    logger.info("Terminé. L'index est prêt.")


if __name__ == "__main__":
    main()
