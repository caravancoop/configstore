import os

from configstore.exceptions import ConfigNotFoundException
SECRETS_PATH = '/run/secrets'


class DockerSecretBackend(object):

    def __init__(self, secrets_path=SECRETS_PATH):
        self.secrets_path = secrets_path

    def get_secret(self, secret):
        path = os.path.join(self.secrets_path, secret)
        if not os.path.exists(path):
            raise ConfigNotFoundException

        with open(path) as fd:
            return fd.readline().strip()
