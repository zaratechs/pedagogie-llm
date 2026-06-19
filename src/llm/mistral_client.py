from mistralai import Mistral
from config.settings import MISTRAL_API_KEY, MISTRAL_MODEL


def get_client() -> Mistral:
    if not MISTRAL_API_KEY:
        raise ValueError("MISTRAL_API_KEY non définie — vérifier le fichier .env")
    return Mistral(api_key=MISTRAL_API_KEY)


def generate(prompt: str) -> str:
    """Envoie un prompt à Mistral et retourne le texte de la réponse."""
    client = get_client()
    response = client.chat.complete(
        model=MISTRAL_MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
