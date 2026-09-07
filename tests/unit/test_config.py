"""Unit tests for configuration loading and data directory resolution."""

import importlib

import pytest

import lotusette.core.config as config_module
from lotusette.core.config import Settings, ensure_directories


def _reload_config(monkeypatch, **env):
    """Reload the config module with a patched environment."""
    for key in ("LOTUSETTE_DATA_DIR", "XDG_DATA_HOME"):
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    return importlib.reload(config_module)


@pytest.fixture(autouse=True)
def _restore_config_module():
    """Leave the module in its pristine state for the other tests."""
    yield
    importlib.reload(config_module)


class TestDefaults:
    """Les valeurs par défaut doivent fonctionner sans aucun .env."""

    def test_default_provider_is_local(self):
        """Lotusette démarre en local, sans clé d'API."""
        settings = Settings(_env_file=None)
        assert settings.llm_provider == "local"
        assert settings.openai_api_key is None
        assert settings.anthropic_api_key is None

    def test_database_defaults_to_sqlite(self):
        """Le défaut est SQLite : aucun serveur à installer.

        Régression : .env.example annonçait un PostgreSQL que config.py
        n'utilisait pas, ce qui cassait toute installation suivant le README.
        """
        settings = Settings(_env_file=None)
        assert settings.database_url.startswith("sqlite:///")
        assert "postgresql" not in settings.database_url

    def test_local_llm_defaults(self):
        """Le serveur local est attendu sur le port 8080."""
        settings = Settings(_env_file=None)
        assert settings.local_llm_base_url == "http://localhost:8080/v1"
        assert settings.local_llm_api_key == "EMPTY"
        assert settings.local_llm_model


class TestEnvironmentOverrides:
    """Lecture des variables d'environnement."""

    def test_local_llm_settings_from_env(self, monkeypatch):
        """Les noms canoniques LOCAL_LLM_* sont lus."""
        monkeypatch.setenv("LOCAL_LLM_BASE_URL", "http://192.168.1.10:9000/v1")
        monkeypatch.setenv("LOCAL_LLM_MODEL", "qwen3-8b")
        monkeypatch.setenv("LOCAL_LLM_API_KEY", "secret")

        settings = Settings(_env_file=None)

        assert settings.local_llm_base_url == "http://192.168.1.10:9000/v1"
        assert settings.local_llm_model == "qwen3-8b"
        assert settings.local_llm_api_key == "secret"

    def test_legacy_vllm_aliases_still_work(self, monkeypatch):
        """Les anciens VLLM_* restent acceptés pour ne pas casser les .env."""
        monkeypatch.setenv("VLLM_BASE_URL", "http://localhost:8001/v1")
        monkeypatch.setenv("VLLM_MODEL", "mistral-7b")
        monkeypatch.setenv("VLLM_API_KEY", "none")

        settings = Settings(_env_file=None)

        assert settings.local_llm_base_url == "http://localhost:8001/v1"
        assert settings.local_llm_model == "mistral-7b"
        assert settings.local_llm_api_key == "none"

    def test_canonical_name_wins_over_alias(self, monkeypatch):
        """Si les deux sont définis, le nom canonique l'emporte."""
        monkeypatch.setenv("LOCAL_LLM_MODEL", "canonique")
        monkeypatch.setenv("VLLM_MODEL", "ancien")

        assert Settings(_env_file=None).local_llm_model == "canonique"

    def test_unknown_variables_are_ignored(self, monkeypatch):
        """Un .env qui traîne des variables obsolètes ne doit pas planter."""
        monkeypatch.setenv("VECTOR_DB_TYPE", "chroma")
        monkeypatch.setenv("UNE_VARIABLE_QUI_NEXISTE_PAS", "42")

        assert Settings(_env_file=None).app_name == "Lotusette"


class TestDataDirectory:
    """Résolution du répertoire de données."""

    def test_import_has_no_filesystem_side_effect(self, monkeypatch, tmp_path):
        """Importer la configuration ne doit rien créer sur le disque.

        Régression : config.py appelait os.makedirs au niveau module.
        """
        target = tmp_path / "pas-encore-la"
        module = _reload_config(monkeypatch, LOTUSETTE_DATA_DIR=str(target))

        assert module.DATA_DIR == target
        assert not target.exists()

    def test_ensure_directories_creates_the_tree(self, monkeypatch, tmp_path):
        """ensure_directories() crée l'arborescence, explicitement."""
        target = tmp_path / "donnees"
        module = _reload_config(monkeypatch, LOTUSETTE_DATA_DIR=str(target))

        module.ensure_directories()

        for subdir in module.DATA_SUBDIRS:
            assert (target / subdir).is_dir()

    def test_ensure_directories_is_idempotent(self, monkeypatch, tmp_path):
        """Appeler deux fois ne lève pas."""
        module = _reload_config(monkeypatch, LOTUSETTE_DATA_DIR=str(tmp_path / "d"))

        module.ensure_directories()
        module.ensure_directories()

    def test_data_dir_stays_outside_the_package(self):
        """Les données ne doivent jamais être écrites dans le package."""
        package_dir = config_module.PROJECT_ROOT / "lotusette"
        assert package_dir not in config_module.DATA_DIR.parents
        assert config_module.DATA_DIR != package_dir

    def test_checkout_uses_repository_data_dir(self):
        """Depuis une copie de travail, on écrit dans <dépôt>/data."""
        assert config_module.DATA_DIR == config_module.PROJECT_ROOT / "data"

    def test_xdg_fallback_when_not_a_checkout(self, monkeypatch, tmp_path):
        """Installé, le paquet écrit sous XDG_DATA_HOME, pas dans site-packages."""
        monkeypatch.setattr(config_module, "PROJECT_ROOT", tmp_path / "site-packages")
        monkeypatch.setenv("XDG_DATA_HOME", str(tmp_path / "xdg"))
        monkeypatch.delenv("LOTUSETTE_DATA_DIR", raising=False)

        assert config_module._resolve_data_dir() == tmp_path / "xdg" / "lotusette"


class TestSecurityValidation:
    """Garde-fou sur la clé secrète."""

    def test_default_secret_key_rejected_in_production(self):
        """La clé par défaut ne doit pas survivre hors mode debug."""
        settings = Settings(_env_file=None, debug=False)
        with pytest.raises(ValueError, match="SECRET_KEY"):
            settings.validate_security()

    def test_default_secret_key_tolerated_in_debug(self):
        """En debug, on ne bloque pas le développeur."""
        Settings(_env_file=None, debug=True).validate_security()

    def test_custom_secret_key_accepted(self):
        """Une vraie clé passe la validation."""
        Settings(_env_file=None, debug=False, secret_key="k" * 32).validate_security()


def test_ensure_directories_is_exported():
    """ensure_directories fait partie de l'API du module."""
    assert callable(ensure_directories)
