try:
    import dotenv
except ImportError:  # pragma: no cover
    dotenv = None
else:
    try:
        dotenv.parse_dotenv
        _parse_dotenv = lambda file: dotenv.parse_dotenv(file.read())
    except AttributeError:  # pragma: no cover
        _parse_dotenv = lambda file: dotenv.dotenv_values(stream=file)


class DotenvBackend:
    """Backend that reads settings in a .env file.

    Create an instance with a path to the .env file.
    """

    def __init__(self, dotenv_path):
        if dotenv is None:
            raise ImportError('no dotenv module found, see instructions in README')

        with open(dotenv_path) as file:
            self.config = _parse_dotenv(file)

    def get_setting(self, key):
        return self.config.get(key)
