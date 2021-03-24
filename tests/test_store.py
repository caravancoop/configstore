import pytest

from configstore import Store, SettingNotFoundException, DictBackend


def test_store_init():
    Store([])
    Store([DictBackend({})])

    with pytest.raises(Exception):
        Store()
    with pytest.raises(Exception):
        Store(None)


def test_store_init_invalid():
    with pytest.raises(TypeError):
        Store([DictBackend])


def test_store_get_setting():
    store = Store([DictBackend({'key': 'secrets!'})])

    value = store.get_setting('key')

    assert value == 'secrets!'


def test_store_get_setting_with_default():
    store = Store([DictBackend({'key': 'secrets!'})])

    value = store.get_setting('key', 'default')

    assert value == 'secrets!'


def test_store_get_setting_missing():
    store = Store([])

    with pytest.raises(SettingNotFoundException):
        store.get_setting('key')


def test_store_get_setting_missing_with_default():
    store = Store([DictBackend({})])

    value = store.get_setting('key', 'default value')

    assert value == 'default value'


def test_store_interpolate():
    store = Store([DictBackend({'environment': 'staging'})])

    s = store.interpolate('before ${environment} after')

    assert s == 'before staging after'


def test_store_interpolate_none_default():
    store = Store([])

    assert store.get_setting('foo', None) is None


def test_store_get_setting_interpolate_value():
    store = Store([DictBackend(dict(
        environment='staging',
        secret_key='42-${environment}-secrets!',
    ))])

    value = store.get_setting('secret_key')

    assert value == '42-staging-secrets!'


def test_store_get_setting_interpolate_missing():
    store = Store([DictBackend({'service_host': 'cool-db-server:6000'})])

    with pytest.raises(SettingNotFoundException):
        store.get_setting('service_url')


def test_store_get_setting_interpolate_default():
    store = Store([DictBackend({'service_host': 'cool-db-server:6000'})])

    value = store.get_setting('service_url', 'https://${service_host}/db')

    assert value == 'https://cool-db-server:6000/db'


def test_store_get_setting_interpolate_special_character_boundary():
    store = Store([DictBackend(dict(
        service_url='https://${user}:${dbpass}@${host}:${port}/${db}',
        user='bob',
        dbpass='secret',
        host='cool-db-server',
        port='6000',
        db='db1',
    ))])

    value = store.get_setting('service_url')

    assert value == 'https://bob:secret@cool-db-server:6000/db1'


def test_store_add_backend():
    store = Store([])

    store.add_backend(DictBackend({'environment': 'staging'}))

    assert store.get_setting('environment') == 'staging'


def test_store_add_backend_invalid():
    class BadBackend:
        def get_key(key):
            """oops wrong name"""

    store = Store([])
    bad = BadBackend()

    with pytest.raises(TypeError):
        store.add_backend(bad)
