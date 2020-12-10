import pytest

from configstore.backends.dict import DictBackend


def test_dict_success():
    d = {'DEBUG': True}

    b = DictBackend(d)
    value = b.get_setting('DEBUG')

    assert value is True


def test_dict_missing():
    b = DictBackend({})
    value = b.get_setting('DATABASE')

    assert value is None
