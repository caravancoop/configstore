class ConfigNotFoundException(Exception):
    pass


_no_default = object()


class Store(object):

    def __init__(self, backends):
        self.backends = list(backends)

    def get_config(self, key, default=_no_default):
        for backend in self.backends:
            try:
                return backend.get_config(key)
            except Exception:
                # Consider any exception as a non-existing secret in
                # this backend
                continue

        if default is not _no_default:
            return default
        else:
            raise ConfigNotFoundException(
                "Couldn't find config {} in any backend".format(key))
