import pytest
import configstore

DOTENV_CONTENTS = u'''
SECRET_KEY=1234dot
ENVIRONMENT=PRODUCTION
export DEBUG=True
'''


def test_env_var_dotenv_success(monkeypatch, tmpdir):
    monkeypatch.setenv('ENVIRONMENT', 'STAGING')
    p = tmpdir.join("config.env")
    p.write(DOTENV_CONTENTS)

    store = configstore.Store([
        configstore.EnvVarBackend(),
        configstore.DotenvBackend(str(p)),
    ])

    secret_key = store.get_setting('SECRET_KEY')
    environment = store.get_setting('ENVIRONMENT')

    assert secret_key == '1234dot'
    assert environment == 'STAGING'

    del store


def test_dotenv_env_var_success(monkeypatch, tmpdir):
    monkeypatch.setenv('ENVIRONMENT', 'STAGING')
    p = tmpdir.join("config.env")
    p.write(DOTENV_CONTENTS)

    store = configstore.Store([
        configstore.DotenvBackend(str(p)),
        configstore.EnvVarBackend(),
    ])

    secret_key = store.get_setting('SECRET_KEY')
    environment = store.get_setting('ENVIRONMENT')

    assert secret_key == '1234dot'
    assert environment == 'PRODUCTION'

    del store


def test_export_success(tmpdir):
    p = tmpdir.join("config.env")
    p.write(DOTENV_CONTENTS)

    store = configstore.Store([
        configstore.DotenvBackend(str(p)),
    ])

    debug = store.get_setting('DEBUG')

    assert debug == 'True'

    del store
