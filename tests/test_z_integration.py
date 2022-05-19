import pytest
import configstore

DOTENV_CONTENTS = u'''
SECRET_KEY=1234dot
ENVIRONMENT=PRODUCTION
EMAIL_DEBUG=1
PROMO2=off
'''

DOTENV_EMPTY = u'''

'''


def test_envvars_override_dotenv(monkeypatch, tmp_path):
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


def test_dotenv_overrides_envvars(monkeypatch, tmp_path):
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


def test_dict_defaults(monkeypatch):
    defaults = {
        'DEBUG': False,
        'TIMEOUT': 100,
    }
    monkeypatch.setenv('TIMEOUT', '5')
    monkeypatch.setenv('EMAIL', 'smtp://localhost')

    store = configstore.Store([
        configstore.EnvVarBackend(),
        configstore.DictBackend(defaults),
    ])

    debug = store.get_setting('DEBUG')
    timeout = int(store.get_setting('TIMEOUT'))
    email = store.get_setting('EMAIL')

    assert debug is False
    assert timeout == 5
    assert email == 'smtp://localhost'


def test_interpolation(monkeypatch, tmp_path):
    monkeypatch.setenv('ENVIRONMENT', 'STAGING')
    monkeypatch.setenv('VERSION', '113')
    monkeypatch.setenv('REDIS_URL', 'https://redis:4012')
    path = tmp_path / 'config.env'
    path.write_text(DOTENV_CONTENTS)
    path.write_text('APP_NAME=supertest-${ENVIRONMENT}-${VERSION}')

    store = configstore.Store([
        configstore.EnvVarBackend(),
        configstore.DotenvBackend(str(path)),
    ])

    environment = store.get_setting('ENVIRONMENT')
    app_name = store.get_setting('APP_NAME')
    session_url = store.get_setting('SESSION_URL', '${REDIS_URL}/2')

    assert environment == 'STAGING'
    assert app_name == 'supertest-STAGING-113'
    assert session_url == 'https://redis:4012/2'


def test_conversion(monkeypatch, tmp_path):
    monkeypatch.setenv('DEBUG', 'on')
    path = tmp_path / 'config.env'
    path.write_text(DOTENV_CONTENTS)

    store = configstore.Store([
        configstore.DotenvBackend(str(path)),
        configstore.EnvVarBackend(),
    ])

    # basic test
    email_as_string = store.get_setting('EMAIL_DEBUG')
    email_as_bool = store.get_setting('EMAIL_DEBUG', asbool=True)

    assert email_as_string == '1'
    assert email_as_bool is True

    # setting found in store, value true
    debug = store.get_setting('DEBUG', asbool=True)
    # not found, default is boolean
    promo1 = store.get_setting('PROMO1', True, asbool=True)
    # found, value false
    promo2 = store.get_setting('PROMO2', asbool=True)
    # not found, default converted from string
    promo3 = store.get_setting('PROMO3', '1', asbool=True)
    # not found, default w/ interpolation, false
    promo3 = store.get_setting('PROMO3', '${PROMO2}', asbool=True)
    # not found, default w/ interpolation, true
    extra_debug = store.get_setting('EXTRA_DEBUG', '${DEBUG}', asbool=True)

    assert debug is True
    assert promo1 is True
    assert promo2 is False
    assert promo3 is False
    assert extra_debug is True

    # error in conversion bubbles up
    with pytest.raises(ValueError):
        store.get_setting('ENVIRONMENT', asbool=True)
