import os
import errno

from .base import Backend

from typing import Optional

SECRETS_PATH = '/run/secrets'


class DockerSecretBackend(Backend):
    """Backend for docker secrets.

    See the documentation for docker services for more info.
    """

    def __init__(self, secrets_path=SECRETS_PATH):
        self.secrets_path = secrets_path

    def get_setting(self, key: str) -> Optional[str]:
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
