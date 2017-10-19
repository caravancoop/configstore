import os


class EnvVarBackend(object):

    def get_config(self, config):
        try:
            return os.environ[config]
        except KeyError:
            return None
