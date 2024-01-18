import pandas as pd
import json
import logging
from io import StringIO
from .utils import get_session

logger = logging.getLogger(__name__)

client = None


class S3Manager:
    def __init__(self):
        """S3Manager Constructor.
        @return: S3 Client.
        """
        logger.info("Creating instance of S3 Client.")
        self.client = get_client()

    def file_exists(self, bucket_name: str, path: str):
        """Check if a file exists.

        @param bucket_name: Bucket name.
        @param path: File S3 path.
        """
        try:
            self.client.head_object(Bucket=bucket_name, Key=path)
            return True
        except:
            return False

    def list_files(self, bucket_name: str, prefix: str = ""):
        """List files in a Bucket.

        @param bucket_name: Bucket name.
        @param prefix: File S3 path for filtering.
        """
        result = self.client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        if "Contents" not in result:
            return []
        return result["Contents"]

    def save_to_s3(self, bucket_name: str, data: str, path: str):
        """Save data in Bucket.

        @param bucket_name: Bucket name.
        @param data: File content.
        @param path: File S3 path.
        """
        return self.client.put_object(Key=path, Body=data, Bucket=bucket_name)

    def save_df_to_s3(
        self,
        bucket_name: str,
        df: pd.DataFrame,
        path: str,
        index: bool = False,
        header: bool = True,
        delimiter: str = ",",
    ):
        """Save a pandas dataframe.

        @param bucket_name: Bucket name.
        @param data: File content.
        @param path: File S3 path.
        """
        buffer = StringIO()
        df.to_csv(buffer, index=index, header=header, sep=delimiter)
        data = buffer.getvalue()
        return self.save_to_s3(bucket_name, data, path)

    def read_csv(self, bucket_name: str, path: str, delimiter: str = ","):
        """Read a CSV in Bucket as pandas dataframe.

        @param bucket_name: Bucket name.
        @param path: File S3 path.
        @param delimiter: CSV delimiter.
        """
        return pd.read_csv(f"s3://{bucket_name}/{path}", sep=delimiter)

    def read_excel(self, bucket_name: str, path: str):
        """Read a Excel in Bucket.

        @param bucket_name: Bucket name.
        @param path: File S3 path.
        """
        path = f"s3://{bucket_name}/{path}"
        return pd.ExcelFile(path, engine="openpyxl")

    def read_excel_sheet(
        self,
        bucket_name: str,
        path: str,
        sheet_name: str,
        skip_header: int = 0,
        usecols: str = "A:Z",
    ):
        """Read a Excel sheet in Bucket as pandas dataframe.

        @param bucket_name: Bucket name.
        @param path: File S3 path.
        @param sheet_name: Excel sheet name.
        @param skip_header: Skip header lines.
        @param usecols: Select sheet columns.
        """
        path = f"s3://{bucket_name}/{path}"
        return pd.read_excel(
            path,
            sheet_name=sheet_name,
            header=skip_header,
            usecols=usecols,
            engine="openpyxl",
        )

    def read_json(self, bucket_name: str, path: str):
        """Read a json in Bucket.

        @param bucket_name: Bucket name.
        @param path: File S3 path.
        """
        obj = self.client.get_object(Bucket=bucket_name, Key=path)
        return json.loads(obj["Body"].read())

    def get_download_url(self, bucket_name: str, path: str, expires=360):
        """Get a signed url for downloading file from S3

        @param bucket_name: Bucket name.
        @param path: File S3 path.
        @param expires: Expiring time.
        """
        url = self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": bucket_name, "Key": path},
            ExpiresIn=expires,
        )
        return url

    def upload_file(self, bucket_name: str, filepath: str, path: str):
        """Upload a file to S3.

        @param bucket_name: Bucket name.
        @param filepath: File source path.
        @param path: File S3 target path.
        """
        self.client.upload_file(filepath, bucket_name, path)

    def upload_file_from_buffer(self, bucket_name: str, buffer: StringIO, path: str):
        """Upload a file from buffer to S3.

        @param bucket_name: Bucket name.
        @param buffer: StringIO buffer file.
        @param path: File S3 target path.
        """
        buffer.seek(0)
        self.client.upload_fileobj(buffer, bucket_name, path)


def get_client():
    """Singleton pattern for getting s3 client."""
    global client
    if client is None:
        client = get_session().client("s3")
    return client
