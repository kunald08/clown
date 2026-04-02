from clown_core.settings import load_settings


def test_load_settings_has_model_name() -> None:
    settings = load_settings()
    assert settings.model_name == "local-echo"
