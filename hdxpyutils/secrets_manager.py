import base64
import boto3
import json
import logging
from .utils import get_session

logger = logging.getLogger(__name__)

cached_secrets = {}
client = None


def get_client(region="us-east-1"):
    global client
    if client is None:
        client = get_session().client(service_name="secretsmanager", region_name=region)
    return client


class SecretsManager:
    def __init__(self, region: str = "us-east-1", cache: bool = True):
        """SecretsManager Constructor.

        @param region: Secrets region.
        @param log: Enables logging.
        @param cache: Enables secrets caching.
        """

        self.region = region
        self.cache = cache
        self.client = get_client()

        logger.info("Creating instance of SecretsManager.")

    def get_secret(self, secret_name: str):
        """Get AWS secret

        @param secret_name: Secret name.
        """

        global cached_secrets

        logger.info(f"Getting secret for {secret_name} in region {self.region}.")

        key = f"{self.region}:{secret_name}"

        if self.cache and key in cached_secrets:
            return cached_secrets[key]
        else:
            response = self.client.get_secret_value(SecretId=secret_name)
            secret = json.loads(
                response["SecretString"]
                if "SecretString" in response
                else base64.b64decode(response["SecretBinary"])
            )
            cached_secrets[key] = secret
            return secret
