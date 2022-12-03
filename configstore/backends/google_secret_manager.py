try:
    from google.cloud import secretmanager
    from google.api_core.exceptions import NotFound
except ImportError:  # pragma: no cover
    secretmanager = None
    NotFound = None


class GoogleSecretManagerBackend:
    """Backend for Google Secrets Manager (GSM).
    """

    def __init__(self, project_id):
        self.project_id = project_id
        self.client = secretmanager.SecretManagerServiceClient()

    def get_setting(self, key):
        """Returns the named secret from GSM"""
        full_name = f"projects/{self.project_id}/secrets/{key}/versions/latest"

        # Access the secret version
        try:
            response = self.client.access_secret_version(name=full_name)
        except NotFound:
            return None

        # Return the decoded payload
        return response.payload.data.decode("UTF-8")
