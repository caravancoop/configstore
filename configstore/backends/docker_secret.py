import os
import errno

SECRETS_PATH = '/run/secrets'


class DockerSecretBackend(object):
    """Backend for docker secrets.

    See the documentation for docker services for more info.
    """

    def __init__(self, secrets_path=SECRETS_PATH):
        self.secrets_path = secrets_path

    def get_setting(self, key):
        path = os.path.join(self.secrets_path, key)

        try:
            file = open(path)
        except IOError as exc:
            if exc.errno == errno.ENOENT:
                return None
            else:
                raise

        with file:
            return file.readline().strip()
