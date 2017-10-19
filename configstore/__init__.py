from configstore.backends import DockerSecretBackend, EnvVarBackend
from configstore.exceptions import ConfigNotFoundException

enabled_backends = [
    DockerSecretBackend(),
    EnvVarBackend()
]

no_default = object()


def get_config(key, default=no_default):
    for backend in enabled_backends:
        try:
            return backend.get_config(key)
        except Exception:
            # Consider any exception as a non-existing secret in this backend
            continue

    if default != no_default:
        return default
    else:
        raise ConfigNotFoundException(
            "Couldn't find config {} in any backend".format(key)
        )
