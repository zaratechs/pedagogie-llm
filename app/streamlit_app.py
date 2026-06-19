import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from sentence_transformers import SentenceTransformer
from src.rag.vectorstore import get_collection
from src.rag.retriever import retrieve_and_generate
from config.settings import EMBEDDING_MODEL

st.set_page_config(
    page_title="Assistant Pédagogique",
    page_icon="📚",
    layout="wide",
)

st.title("📚 Assistant Pédagogique — Collégial")
st.caption("Propulsé par vos ressources pédagogiques + Mistral AI")


@st.cache_resource
def load_resources():
    model = SentenceTransformer(EMBEDDING_MODEL)
    collection = get_collection()
    return model, collection


model, collection = load_resources()

mode = st.selectbox(
    "Type de demande",
    ["Stratégie pédagogique", "Grille d'évaluation", "Outil d'animation"],
)

question = st.text_area(
    "Décris ton contexte ou ta question",
    height=120,
    placeholder=(
        "Ex. : Je donne un premier cours de chimie organique à des étudiants "
        "en sciences de la santé. Quelle stratégie pour introduire les groupes fonctionnels ?"
    ),
)

if st.button("Générer", type="primary") and question.strip():
    with st.spinner("Recherche dans la base de connaissances..."):
        full_question = f"[{mode}] {question}"
        result = retrieve_and_generate(full_question, model, collection)

    st.markdown("### Réponse")
    st.markdown(result["answer"])

    with st.expander("Sources utilisées"):
        for src in result["sources"]:
            st.write(f"- `{src['type']}` — {src['source']}")
