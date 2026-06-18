def test_settings_paths_exist_after_creation(tmp_path, monkeypatch):
    """Les chemins de settings sont des Path objects et pointent sous le projet."""
    monkeypatch.setenv("MISTRAL_API_KEY", "test-key")
    from config import settings
    assert settings.ROOT_DIR.is_dir()
    assert str(settings.DATA_DIR).endswith("data")
    assert settings.CHUNK_SIZE == 500
    assert settings.CHUNK_OVERLAP == 50
    assert settings.TOP_K_CHUNKS == 5
    assert settings.MISTRAL_MODEL == "mistral-small-latest"
