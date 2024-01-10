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
        client = get_session().client(service_name="lambda", region_name=region)
    return client


class LambdaManager:
    def __init__(self):
        """LambdaManager Constructor.
        
        @return: LambdaManager instance.
        """
        self.client = get_client()

        logger.info("Creating instance of LambdaManager.")

    def invoke(self, function_name, params=None, context={}, asynchronous=False):
        """Invoke a lambda function.
        @param function_name: Lambda function name.
        @param params: Lambda function parameters.
        @param context: Lambda function context.
        @param asynchronous: Invoke lambda function asynchronously.
        @return: Lambda function result.
        """
        response = self.client.invoke(
            FunctionName=function_name,
            InvocationType="Event" if asynchronous else "RequestResponse",
            LogType="None",
            ClientContext=self.create_lambda_context(**context),
            Payload="{}" if params is None else json.dumps(params),
        )

        result = json.loads(response["Payload"].read().decode())

        return result

    def create_lambda_context(self, custom=None, env=None, client=None):
        """Create a lambda context.
        @param custom: Custom context.
        @param env: Environment context.
        @param client: Client context.
        @return: Lambda context.
        """
        client_context = dict(custom=custom, env=env, client=client)
        json_context = json.dumps(client_context).encode("utf-8")
        return base64.b64encode(json_context).decode("utf-8")
