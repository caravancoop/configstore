try:
    from google.cloud import secretmanager
    from google.api_core.exceptions import NotFound
except ImportError:  # pragma: no cover
    secretmanager = None
    NotFound = None


class GoogleSecretManagerBackend:
    """Backend for Google Secrets Manager (GSM).
    """

    def __init__(self, project_id: str, cache_keys: str):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

        # If cache_keys is true, we load a list of all keys at init time. This
        # will make things a lot quicker when trying to load a key that doesn't exist
        if cache_keys:
            self.cached_keys = self._list()
        else:
            self.cached_keys = None

    def _list(self) -> set[str]:
        """Lists all the names of secrets stored in an environment"""
        parent = f"projects/{self.project_id}"
        results = self.client.list_secrets(parent=parent)
        return {response.name.split("/")[-1] for response in results}

    def _get(self, key: str) -> str:
        full_name = f"projects/{self.project_id}/secrets/{key}/versions/latest"

        # Access the secret version
        try:
            response = self.client.access_secret_version(name=full_name)
        except NotFound:
            return None

        # Return the decoded payload
        return response.payload.data.decode("UTF-8")

    def get_setting(self, key: str) -> str:
        """Returns the named item from GSM,
        optionally checking a cached list of keys that exist before doing
        so"""
        # If we have cached a list of keys, check that list before
        # trying to load a variable. This will speed things up a lot
        # in the case where the key doesn't exist
        if self.cached_keys is not None:
            if key not in self.cached_keys:
                return None

        return self._get(key)
