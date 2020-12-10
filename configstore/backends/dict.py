class DictBackend:
    """Simple backend to populate settings from a dictionary."""

    def __init__(self, settings):
        self._settings = settings
        # we're not making a copy or deep copy here; intended usage is
        # to create a dict on the fly (like DictBackend({"key": value})).
        # passing a dict that survives and can be mutated is possible.

    def get_setting(self, key):
        return self._settings.get(key)
