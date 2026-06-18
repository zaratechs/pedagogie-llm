"""Télécharge le modèle d'embedding une seule fois. Lancer avant build_index.py."""
from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

print(f"Téléchargement du modèle : {EMBEDDING_MODEL}")
print("Taille approximative : 400 Mo — première exécution seulement.")
model = SentenceTransformer(EMBEDDING_MODEL)
print("Modèle téléchargé et mis en cache.")
