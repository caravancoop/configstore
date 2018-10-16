from typing import TypeVar, Union, Tuple, Iterable

from .backends.env_var import EnvVarBackend
from .backends.dotenv import DotenvBackend
from .backends.awsssm import AwsSsmBackend
from .backends.docker_secret import DockerSecretBackend


Backends = TypeVar('Backends', EnvVarBackend, DotenvBackend,
                   AwsSsmBackend, DockerSecretBackend)


class SettingNotFoundException(Exception):
    pass


_no_default = object()


class Store(object):

    def __init__(self, backends) -> None:
        self._backends = tuple(backends)

    def add_backend(self, backend: Backends):
        self._backends += (backend,)

    def get_setting(self, key: str, default=_no_default) -> str:
        for backend in self._backends:
            ret = backend.get_setting(key)
            if ret is None:
                continue

            return ret

        if default is not _no_default:
            return default
        else:
            raise SettingNotFoundException(
                "Couldn't find setting {} in any backend".format(key))
