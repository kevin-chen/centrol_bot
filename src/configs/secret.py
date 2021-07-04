from google.cloud import secretmanager
from google.auth import credentials
import logging

log = logging.getLogger(__name__)


class GoogleSecret:

    project_id = "1001398086066"
    default_version = "latest"

    def __init__(self):

        self.client = secretmanager.SecretManagerServiceClient()

    def access_secret(self, secret_id: str) -> str:
        """
        Access the payload for the given secret version if one exists. The version
        can be a version number as a string (e.g. "5") or an alias (e.g. "latest").
        """

        # Build the resource name of the secret version.
        name = f"projects/{self.project_id}/secrets/{secret_id}/versions/{self.default_version}"

        # Access the secret version.
        response = self.client.access_secret_version(request={"name": name})

        try:
            payload = response.payload.data.decode("UTF-8")
            return payload
        except Exception as e:
            log.error(f"Failed to get secret. {e}")
