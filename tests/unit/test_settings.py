from company_ai.config.settings import Settings


def test_default_settings():
    settings = Settings()

    assert settings.app_name == "company-ai-analyst"
    assert settings.app_env == "development"
    assert settings.debug is False



def test_settings_from_environment(monkeypatch):
    monkeypatch.setenv("APP_NAME", "test-app")
    monkeypatch.setenv("APP_ENV", "test")

    settings = Settings()

    assert settings.app_name == "test-app"
    assert settings.app_env == "test"