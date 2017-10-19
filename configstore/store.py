from configstore import DockerSecretBackend, EnvVarBackend
from configstore.exceptions import ConfigNotFoundException

DEFAULT_BACKENDS = [
    DockerSecretBackend(),
    EnvVarBackend()
]

NO_DEFAULT = object()


class Store(object):

    def __init__(self, backends=DEFAULT_BACKENDS):
        self.backends = backends

    def get_config(self, key, default=NO_DEFAULT):
        for backend in self.backends:
            try:
                return backend.get_config(key)
            except Exception:
                # Consider any exception as a non-existing secret in
                # this backend
                continue

        if default != NO_DEFAULT:
            return default
        else:
            raise ConfigNotFoundException(
                "Couldn't find config {} in any backend".format(key)
            )
