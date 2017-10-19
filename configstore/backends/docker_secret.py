import os

SECRETS_PATH = '/run/secrets'


class DockerSecretBackend(object):

    def __init__(self, secrets_path=SECRETS_PATH):
        self.secrets_path = secrets_path

    def get_config(self, key):
        path = os.path.join(self.secrets_path, key)

        if not os.path.exists(path):
            return None

        with open(path) as fd:
            return fd.readline().strip()
