import os


class EnvVarBackend(object):
    """Backend that reads settings in environment variables."""

    def get_setting(self, config):
        return os.environ.get(config)
