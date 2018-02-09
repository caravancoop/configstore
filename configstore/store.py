class SettingNotFoundException(Exception):
    pass


_no_default = object()


class Store(object):

    def __init__(self, backends):
        self._backends = tuple(backends)

    def add_backend(self, backend):
        self._backends += (backend,)

    def get_setting(self, key, default=_no_default):
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
