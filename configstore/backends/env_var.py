import os


class EnvVarBackend(object):

    def get_secret(self, secret):
        # If this raises KeyError it will be caught upstream
        return os.environ[secret]
