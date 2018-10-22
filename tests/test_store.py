import pytest

from configstore import Store, SettingNotFoundException


class DictBackend:
    def __init__(self, **settings):
        self._settings = settings

    def get_setting(self, key):
        return self._settings.get(key)


def test_store_init():
    Store([])
    Store([DictBackend()])
    # This error is not caught at the moment
    Store([DictBackend])

    with pytest.raises(Exception):
        Store()
    with pytest.raises(Exception):
        Store(None)


def test_store_get_setting():
    store = Store([DictBackend(key='secrets!')])

    value = store.get_setting('key')

    assert value == 'secrets!'


def test_store_get_setting_with_default():
    store = Store([DictBackend(key='secrets!')])

    value = store.get_setting('key', 'default')

    assert value == 'secrets!'


def test_store_get_setting_missing():
    store = Store([])

    with pytest.raises(SettingNotFoundException):
        store.get_setting('key')


def test_store_get_setting_missing_with_default():
    store = Store([DictBackend()])

    value = store.get_setting('key', 'default value')

    assert value == 'default value'


def test_store_add_backend():
    store = Store([])

    store.add_backend(DictBackend(environment='staging'))

    assert store.get_setting('environment') == 'staging'
