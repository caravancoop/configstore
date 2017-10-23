import os


class EnvVarBackend(object):

    def get_config(self, config):
        return os.environ.get(config)
