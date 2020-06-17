import re


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

    Interpolation is supported: include a setting value in another setting
    by surrounding the setting name with "${" and "}", example:

        # base setting
        redis_url = https://redis/
        stats_url = ${redis_url}1
        # => stats_url is https://redis/1
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

            if "${" in ret:
                ret = self.interpolate(ret)

            return ret

        if default is not _no_default:
            if "${" in default:
                return self.interpolate(default)
            return default
        else:
            raise SettingNotFoundException(
                "Couldn't find setting {} in any backend".format(key)
            )

    def get_boolean(self, key, default=False):
        value = self.get_setting(key, str(default))
        return value.lower() in self.boolean_values

    def interpolate(self, string):
        res = re.sub(r"\$\{([_a-zA-Z0-9]+)\}", self._replace, string, count=1)
        return res

    def _replace(self, matchobj):
        key = matchobj.group(1)
        return self.get_setting(key)
