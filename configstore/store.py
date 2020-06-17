class SettingNotFoundException(Exception):
    """Error raised for settings not found in any backend and without default value."""


_no_default = object()

default_boolean_values = {'true', 't', 'yes', 'y', '1'}


class Store(object):
    """A collection of backends that let you retrieve settings from them.

    Backends can be passed to constructor and/or added with add_backend.
    When get_setting is called, backends are searched in addition order
    to find the value; if no backend returns a value and the method was
    called without a default, SettingNotFoundException is raised.
    """

    def __init__(self, backends, boolean_values=default_boolean_values):
        self._backends = tuple(backends)
        self.boolean_values = set()
        for value in boolean_values:
            self.add_boolean_value(value)

    def add_backend(self, backend):
        self._backends += (backend,)

    def add_boolean_value(self, value):
        self.boolean_values.add(str(value).lower())

    def get_setting(self, key, default=_no_default):
        for backend in self._backends:
            ret = backend.get_setting(key)
            if ret is None:
                continue

            return ret

        if default is not _no_default:
            return default
        else:
            raise SettingNotFoundException(
                "Couldn't find setting {} in any backend".format(key)
            )

    def get_boolean(self, key, default=False):
        value = self.get_setting(key, str(default))
        return value.lower() in self.boolean_values
