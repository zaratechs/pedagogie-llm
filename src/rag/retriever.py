from sentence_transformers import SentenceTransformer
import chromadb
from config.settings import TOP_K_CHUNKS, MAX_CONTEXT_CHARS
from src.rag.vectorstore import query_collection
from src.llm.mistral_client import generate

PROMPT_TEMPLATE = """Tu es un assistant pédagogique spécialisé dans l'enseignement collégial québécois.
Réponds en français. Base ta réponse uniquement sur les extraits suivants.

CONTEXTE :
{context}

QUESTION DE L'ENSEIGNANT :
{question}

RÉPONSE :"""


def retrieve_and_generate(
    question: str,
    model: SentenceTransformer,
    collection: chromadb.Collection,
    top_k: int = TOP_K_CHUNKS,
) -> dict:
    """Pipeline RAG complet : vectorise la question → récupère les chunks → génère la réponse."""
    query_embedding = model.encode(question).tolist()
    chunks = query_collection(collection, query_embedding, top_k=top_k)

    context_parts = []
    total_chars = 0
    for chunk in chunks:
        if total_chars + len(chunk["text"]) > MAX_CONTEXT_CHARS:
            break
        context_parts.append(f"[Source : {chunk['source']}]\n{chunk['text']}")
        total_chars += len(chunk["text"])

    context = "\n\n---\n\n".join(context_parts)
    prompt = PROMPT_TEMPLATE.format(context=context, question=question)
    answer = generate(prompt)

    return {
        "answer": answer,
        "sources": [
            {"source": c["source"], "type": c["type"]}
            for c in chunks[:len(context_parts)]
        ],
    }
