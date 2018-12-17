import pytest

from configstore.backends.base import Backend


def test_backend_get_setting_is_not_implemented():
    backend = Backend()

    with pytest.raises(NotImplementedError):
        backend.get_setting('test')
