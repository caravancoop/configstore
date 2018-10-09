import io
import sys
import errno

import pretend
import pytest

from configstore.backends.docker_secret import DockerSecretBackend


if sys.version_info[0] == 3:
    builtins_open = 'builtins.open'
else:  # pragma: no cover
    builtins_open = '__builtin__.open'


def test_docker_secret_success(monkeypatch):
    fake_open = pretend.call_recorder(lambda path: io.StringIO(u'sup3r s3cr3t'))
    # StringIO implements __enter__, so our one-liner works for "with open(path)"
    monkeypatch.setattr(builtins_open, fake_open)

    b = DockerSecretBackend()
    value = b.get_setting('APP_SECRET_KEY')

    assert value == 'sup3r s3cr3t'
    assert fake_open.calls == [pretend.call('/run/secrets/APP_SECRET_KEY')]


def test_docker_secret_missing(monkeypatch):
    b = DockerSecretBackend('/does/not/exist/at/all')
    value = b.get_setting('APP_SECRET_KEY')

    assert value is None


def test_docker_secret_bad_config(monkeypatch):
    exc = OSError(errno.EISDIR, 'is a dir')
    fake_open = pretend.call_recorder(pretend.raiser(exc))
    monkeypatch.setattr(builtins_open, fake_open)

    b = DockerSecretBackend()
    with pytest.raises(OSError):
        b.get_setting('APP_SECRET_KEY')


def test_docker_secret_custom_path_success(monkeypatch):
    fake_open = pretend.call_recorder(lambda path: io.StringIO(u'wow s3cr3t'))
    monkeypatch.setattr(builtins_open, fake_open)

    b = DockerSecretBackend('/custom/path')
    value = b.get_setting('APP_SECRET_KEY')

    assert value == 'wow s3cr3t'
    assert fake_open.calls == [pretend.call('/custom/path/APP_SECRET_KEY')]
