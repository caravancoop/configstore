import os

from .base import Backend


class EnvVarBackend(Backend):

    def get_setting(self, config):
        return os.environ.get(config)
