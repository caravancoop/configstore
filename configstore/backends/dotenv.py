from __future__ import absolute_import

from .base import Backend

from typing import Optional

try:
    import dotenv  # pyre-ignore
except ImportError:  # pragma: no cover
    dotenv = None


class DotenvBackend(Backend):
    """Backend that reads settings in a .env file.

    Create an instance with a path to the .env file.
    """

    def __init__(self, dotenv_path):
        if dotenv is None:
            raise ImportError('install configstore[dotenv] to use the dotenv backend')

        with open(dotenv_path) as file:
            content = file.read()

        self.config = dotenv.parse_dotenv(content)

    def get_setting(self, key: str) -> Optional[str]:
        return self.config.get(key)
