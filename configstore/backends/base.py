from typing import Optional


class Backend(object):

    def __init__(self) -> None:
        pass

    def get_setting(self, key: str) -> Optional[str]:
        raise NotImplementedError
