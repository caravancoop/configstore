import re

from . import converters


class SettingNotFoundException(Exception):
    """Error raised for settings not found in any backend and without default value."""


_no_default = object()


class Store:
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

    A keyword-only parameter can automatically convert string values
    to booleans: true, on, yes, 1 / false, off, no, 0, empty string

        # string setting
        debug_email = OFF
        # => debug_email is False
    """

    def __init__(self, backends):
        self._backends = ()
        for backend in backends:
            self.add_backend(backend)

    def add_backend(self, backend):
        if isinstance(backend, type):
            raise TypeError(
                f"backend can't be a class, did you forget parentheses? {backend!r}"
            )
        if not callable(getattr(backend, "get_setting", None)):
            raise TypeError(
                f"invalid backend {backend!r} does not have get_setting method"
            )
        self._backends += (backend,)

    def get_setting(self, key, default=_no_default, *, asbool=False):
        ret = None
        for backend in self._backends:
            ret = backend.get_setting(key)
            if ret is not None:
                break

        if ret is None and default is _no_default:
            raise SettingNotFoundException(
                "Couldn't find setting {} in any backend".format(key)
            )
        elif ret is None:
            ret = default

        if isinstance(ret, str) and "${" in ret:
            ret = self.interpolate(ret)

        if asbool:
            ret = converters.asbool(ret)

        return ret

    def interpolate(self, string):
        res = re.sub(r"\$\{([_a-zA-Z0-9]+)\}", self._replace, string)
        return res

    def _replace(self, matchobj):
        key = matchobj.group(1)
        return self.get_setting(key)
