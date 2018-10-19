import io
import sys

import pretend
import pytest

from configstore.backends.dotenv import DotenvBackend


if sys.version_info[0] == 3:
    builtins_open = 'builtins.open'
else:  # pragma: no cover
    builtins_open = '__builtin__.open'


def test_dotenv_init_bad_install(monkeypatch):
    monkeypatch.setattr('configstore.backends.dotenv.dotenv', None)

    with pytest.raises(ImportError):
        DotenvBackend('/secrets/app')


def test_dotenv_init_bad_file(monkeypatch):
    with pytest.raises(IOError):
        DotenvBackend('/this/does/not/exist')

    with pytest.raises(IOError):
        DotenvBackend('/home')


def test_dotenv_success(monkeypatch):
    content = u'APP_SECRET_KEY=1234abcd'
    fake_open = pretend.call_recorder(lambda path: io.StringIO(content))
    monkeypatch.setattr(builtins_open, fake_open)

    b = DotenvBackend('/some/path')
    value = b.get_setting('APP_SECRET_KEY')

    assert value == '1234abcd'
    assert fake_open.calls == [pretend.call('/some/path')]


def test_dotenv_missing(monkeypatch):
    content = u'APP_SECRET_KEY=1234abcd'
    fake_open = lambda path: io.StringIO(content)
    monkeypatch.setattr(builtins_open, fake_open)

    b = DotenvBackend('/some/path')
    value = b.get_setting('APP_DEBUG')

    assert value is None
