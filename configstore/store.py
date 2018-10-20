from typing import Type

from .backends import Backend


class SettingNotFoundException(Exception):
    pass


_no_default: str = '~~!!configstore-no-default!!~~'


class Store(object):

    def __init__(self, backends) -> None:
        self._backends = tuple(backends)

    def add_backend(self, backend: Type[Backend]):
        self._backends += (backend,)

    def get_setting(self, key: str, default: str=_no_default) -> str:
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
