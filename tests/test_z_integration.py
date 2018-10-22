import pytest
import configstore

DOTENV_CONTENTS = u'''
SECRET_KEY=1234dot
ENVIRONMENT=PRODUCTION
'''

DOTENV_EMPTY = u'''

'''


def test_configstore_envvars_override_dotenv(monkeypatch, tmp_path):
    monkeypatch.setenv('ENVIRONMENT', 'STAGING')
    path = tmp_path / 'config.env'
    path.write_text(DOTENV_CONTENTS)

    store = configstore.Store([
        configstore.EnvVarBackend(),
        configstore.DotenvBackend(str(path)),
    ])

    secret_key = store.get_setting('SECRET_KEY')
    environment = store.get_setting('ENVIRONMENT')

    assert secret_key == '1234dot'
    assert environment == 'STAGING'


def test_configstore_dotenv_overrides_envvars(monkeypatch, tmp_path):
    monkeypatch.setenv('ENVIRONMENT', 'STAGING')
    path = tmp_path / 'config.env'
    path.write_text(DOTENV_CONTENTS)

    store = configstore.Store([
        configstore.DotenvBackend(str(path)),
        configstore.EnvVarBackend(),
    ])

    secret_key = store.get_setting('SECRET_KEY')
    environment = store.get_setting('ENVIRONMENT')

    assert secret_key == '1234dot'
    assert environment == 'PRODUCTION'


def test_dotenv_empty_file(monkeypatch, tmp_path):
    monkeypatch.setenv('ENVIRONMENT', 'STAGING')
    path = tmp_path / 'config.env'
    path.write_text(DOTENV_EMPTY)

    store = configstore.Store([
        configstore.DotenvBackend(str(path)),
        configstore.EnvVarBackend(),
    ])

    with pytest.raises(Exception) as excinfo:
        store.get_setting('DEBUG')
    environment = store.get_setting('ENVIRONMENT')

    assert "Couldn't find setting" in str(excinfo.value)
    assert environment == 'STAGING'
