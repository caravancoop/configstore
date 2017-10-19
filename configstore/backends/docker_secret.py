import os

SECRETS_PATH = '/run/secrets'


class DockerSecretBackend(object):

    def __init__(self, secrets_path=SECRETS_PATH):
        self.secrets_path = secrets_path

    def get_config(self, key):
        path = os.path.join(self.secrets_path, key)

        try:
            with open(path) as fd:
                return fd.readline().strip()
        except FileNotFoundError:
            return None
