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


def test_interpolation(monkeypatch, tmp_path):
    monkeypatch.setenv('ENVIRONMENT', 'STAGING')
    monkeypatch.setenv('REDIS_URL', 'https://redis:4012')
    #monkeypatch.setenv('APP_NAME', 'supertest-${ENVIRONMENT}-1')
    path = tmp_path / 'config.env'
    path.write_text(DOTENV_CONTENTS)
    path.write_text('APP_NAME=supertest-${ENVIRONMENT}-1')

    store = configstore.Store([
        configstore.EnvVarBackend(),
        configstore.DotenvBackend(str(path)),
    ])

    environment = store.get_setting('ENVIRONMENT')
    app_name = store.get_setting('APP_NAME')
    session_url = store.get_setting('SESSION_URL', '${REDIS_URL}/2')

    assert environment == 'STAGING'
    assert app_name == 'supertest-STAGING-1'
    assert session_url == 'https://redis:4012/2'
