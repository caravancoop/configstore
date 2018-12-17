import os

from .base import Backend

from typing import Optional


class EnvVarBackend(Backend):
    """Backend that reads settings in environment variables."""

    def get_setting(self, key: str) -> Optional[str]:
        return os.environ.get(key)
