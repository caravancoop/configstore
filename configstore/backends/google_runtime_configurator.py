try:
    from google.cloud import runtimeconfig
except ImportError:  # pragma: no cover
    runtimeconfig = None


class GoogleRuntimeConfiguratorBackend:
    """Backend for Google Runtime Configurator.
    """

    def __init__(self, project_id, config_name):
        client = runtimeconfig.Client(project=project_id)
        self.config = client.config(config_name)

    def get_setting(self, key):
        """Returns the named item from runtime configurator"""
        variable = self.config.get_variable(key)

        if variable is None:
            return None
        else:
            return variable.text
