import pytest
from unittest.mock import patch, MagicMock


def test_generate_retourne_le_texte_de_la_reponse():
    """generate() retourne le contenu texte de la réponse Mistral."""
    from src.llm.mistral_client import generate

    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Voici une stratégie pédagogique."

    with patch("src.llm.mistral_client.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.chat.complete.return_value = mock_response
        mock_get_client.return_value = mock_client

        result = generate("Propose une stratégie pour un cours de chimie.")

    assert result == "Voici une stratégie pédagogique."


def test_generate_transmet_le_bon_modele(monkeypatch):
    """generate() utilise le modèle défini dans settings."""
    from src.llm import mistral_client

    monkeypatch.setattr(mistral_client, "MISTRAL_MODEL", "mistral-small-latest")
    monkeypatch.setattr(mistral_client, "MISTRAL_API_KEY", "fake-key")

    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Réponse."

    with patch("src.llm.mistral_client.Mistral") as mock_mistral_class:
        mock_client = MagicMock()
        mock_client.chat.complete.return_value = mock_response
        mock_mistral_class.return_value = mock_client

        mistral_client.generate("Question ?")

        call_kwargs = mock_client.chat.complete.call_args.kwargs
        assert call_kwargs["model"] == "mistral-small-latest"


def test_get_client_leve_erreur_sans_cle(monkeypatch):
    """get_client() lève ValueError si MISTRAL_API_KEY est absente."""
    from src.llm import mistral_client

    monkeypatch.setattr(mistral_client, "MISTRAL_API_KEY", None)

    with pytest.raises(ValueError, match="MISTRAL_API_KEY"):
        mistral_client.get_client()
