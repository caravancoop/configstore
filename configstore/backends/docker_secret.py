import os

from configstore.exceptions import ConfigNotFoundException
SECRETS_PATH = '/run/secrets'


class DockerSecretBackend(object):

    def __init__(self, secrets_path=SECRETS_PATH):
        self.secrets_path = secrets_path

    def get_secret(self, secret):

        with open(os.path.join(self.secrets_path, secret)) as fd:
            return fd.readline().strip()
