import pytest

from .. import Store, SettingNotFoundException


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


def test_store_success():
    store = Store([DictBackend(key='secrets!')])

    value = store.get_setting('key')

    assert value == 'secrets!'


def test_store_success_with_default():
    store = Store([DictBackend(key='secrets!')])

    value = store.get_setting('key', 'default')

    assert value == 'secrets!'


def test_store_missing():
    store = Store([])

    with pytest.raises(SettingNotFoundException):
        store.get_setting('key')


def test_store_missing_with_default():
    store = Store([DictBackend()])

    value = store.get_setting('key', 'default value')

    assert value == 'default value'
