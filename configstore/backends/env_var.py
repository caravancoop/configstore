import os


class EnvVarBackend:
    """Backend that reads settings in environment variables."""

    def get_setting(self, key):
        return os.environ.get(key)
