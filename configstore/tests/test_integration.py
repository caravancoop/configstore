import pytest

import configstore

DOTENV_CONTENTS = u'''
APP_SECRET_KEY=1234dot
APP_ENVIRONMENT=PRODUCTION
'''


def test_env_var_dotenv_success(monkeypatch, tmpdir):
    monkeypatch.setenv('APP_ENVIRONMENT', 'STAGING')
    p = tmpdir.join("config.env")
    p.write(DOTENV_CONTENTS)

    store = configstore.Store([
        configstore.EnvVarBackend(),
        configstore.DotenvBackend(p),
    ])

    app_environment = store.get_setting('APP_ENVIRONMENT')
    app_secret_key = store.get_setting('APP_SECRET_KEY')

    assert app_secret_key == '1234dot'
    assert app_environment == 'STAGING'

    del store
