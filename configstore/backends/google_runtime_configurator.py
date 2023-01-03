try:
    from google.cloud import runtimeconfig
except ImportError:  # pragma: no cover
    runtimeconfig = None


class GoogleRuntimeConfiguratorBackend:
    """Backend for Google Runtime Configurator.
    """

    def __init__(self, project_id: str, config_name: str, cache_keys: bool):
        client = runtimeconfig.Client(project=project_id)
        self.config = client.config(config_name)

        # If cache_keys is true, we load a list of all keys at init time. This
        # will make things a lot quicker when trying to load a key that doesn't exist
        if cache_keys:
            self.cached_keys = self._list()
        else:
            self.cached_keys = None

    def _list(self) -> set[str]:
        """Lists all the keys of items stored in an environment"""
        variables = self.config.list_variables()
        return {variable.name for variable in list(variables)}

    def _get(self, key) -> str:
        """Low level method to get setting from runtime configurator"""
        variable = self.config.get_variable(key)

        if variable is None:
            return None
        else:
            return variable.text

    def get_setting(self, key) -> str:
        """Returns the named item from runtime configurator,
        optionally checking a cached list of keys that exist before doing
        so"""

        # If we have cached a list of keys, check that list before
        # trying to load a variable. This will speed things up a lot
        # in the case where the key doesn't exist
        if self.cached_keys is not None:
            if key not in self.cached_keys:
                return None

        return self._get(key)
