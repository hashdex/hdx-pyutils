import hdxpyutils
import requests, requests.auth
import logging

logger = logging.getLogger(__name__)


class InoaApiManager:
    def __init__(self, secret_name: str):
        """InoaApi Constructor.

        @param secret: Secret name from AWS - Secret Manager.
        """
        secret_manager = hdxpyutils.SecretsManager()
        secret = secret_manager.get_secret(secret_name)

        self.api_path = secret["inoa_url"] + secret["inoa_path_api"]
        self.auth = requests.auth.HTTPBasicAuth(
            secret["username"], secret["password"]
        )
        logger.info("Creating instance of INOA API Client.")

    def call(self, module: str, method: str, params: dict = {}):
        """Makes request to inoa server.

        @param module (string): Module name.
        @param method (string): Method name.
        @param params (dict): Request params.
        """

        endpoint = f"{self.api_path}/{module}/{method}"

        logger.info(f"Sending request to {endpoint}")

        r = requests.post(endpoint, json=params, auth=self.auth)

        logger.info(f"Response status code: {r.status_code}")
        logger.info(f"Response content (truncated): {r.content[:100]}...")

        r.raise_for_status()
        response = r.json()
        return response
