from boto3.dynamodb.types import TypeDeserializer
from . import get_session
import logging

logger = logging.getLogger(__name__)

deserializer = TypeDeserializer()
client = None


class DynamodbManager:
    def __init__(self):
        logger.info("Creating instance of Dynamodb Client.")
        self.client = get_client()

    def pql_query(self, pql_string: str, limit: int = 3000):
        """Query dynamodb using a PartiQL query language.

        @param pql_string: PartiQL query string.
        @param limit: Truncate number of items returned.
        """
        data = self.client.execute_statement(Statement=pql_string)
        items = self.deserialize_items(data["Items"][:limit])
        return {"items": items, "count": len(items)}

    def query(self, table: str, **kwargs):
        """Query dynamodb table.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.query

        @param table: Table name.
        """
        data = self.client.query(TableName=table, **kwargs)
        items = self.deserialize_items(data["Items"])
        return {"items": items, "count": len(items)}

    def scan(self, table: str, **kwargs):
        """Scans dynamodb table.
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan

        @param table: Table name.
        """
        data = self.client.scan(TableName=table, **kwargs)
        if "Items" not in data:
            return data
        items = self.deserialize_items(data["Items"])
        return {"items": items, "count": len(items)}

    def get_item(self, table: str, keys: dict):
        """Get an item from a dynamodb table.

        @param table: dynamodb table name.
        @param keys: dict of key:values that uniquely identify the item.
        """
        data = self.serialize(keys)
        response = self.client.get_item(TableName=table, Key=data)
        if (
            "Item" not in response
            and response["ResponseMetadata"]["HTTPStatusCode"] == 200
        ):
            return None
        return self.deserialize(response["Item"])

    def put_item(self, table: str, item: dict):
        """Put an item in a dynamodb table.
        Current supported column types:
          - string, number, boolean, list of strings, list of numbers, map.

        @param table: dynamodb table name.
        @item item: item to be inserted. (dict of key:values)
        """
        data = self.serialize(item)
        self.client.put_item(TableName=table, Item=data)
        return True

    def delete_item(self, table: str, keys: dict):
        """Delete an item from a dynamodb table.

        @param table: dynamodb table name.
        @param keys: dict of key:values that uniquely identify the item.
        """
        data = self.serialize(keys)
        self.client.delete_item(TableName=table, Key=data)
        return True

    def serialize(self, item: dict):
        """Used for serializing an item when saving in a dynamo table.

        @param item: dict of key:values.
        """
        data = {}
        for key, value in item.items():
            vtype = type(value)
            if vtype is int or vtype is float:
                data[key] = {"N": str(value)}
            elif vtype is bool:
                data[key] = {"BOOL": value}
            elif vtype is list or vtype is tuple or vtype is range:
                if len(value) > 0:
                    if type(value[0]) is int or type(value[0]) is float:
                        data[key] = {"NS": value}
                    else:
                        data[key] = {"SS": [str(v) for v in value]}
                else:
                    data[key] = {"SS": []}
            elif vtype is dict:
                data[key] = {"M": value}
            else:
                data[key] = {"S": value}
        return data

    def deserialize(self, item: dict):
        """Used for deserializing an item when reading a dynamodb table.

        @param item: dict of key:values.
        """
        return {
            k: float(v["N"]) if "N" in v else deserializer.deserialize(value=v)
            for k, v in item.items()
        }

    def deserialize_items(self, items: list):
        """Used for deserializing a list of items.

        @param items: list of dict of key:values.
        """
        return [self.deserialize(item) for item in items]


def get_client():
    """Singleton pattern for getting dynamodb client.

    @returns dynamodb client.
    """
    global client
    if client is None:
        client = get_session().client("dynamodb")
    return client
