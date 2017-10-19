import os


class EnvVarBackend(object):

    def get_config(self, config):
        # If this raises KeyError it will be caught upstream
        return os.environ[config]
