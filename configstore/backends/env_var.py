import os


class EnvVarBackend(object):

    def get_setting(self, config):
        return os.environ.get(config)
