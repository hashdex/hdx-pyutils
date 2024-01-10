from pyathena import connect
import hdxpyutils
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class DatalakeManager:
    def __init__(self, secret_name: str, s3_dir: str, region: str = "us-east-1"):
        """DatalakeManager Constructor.

        @param secret_name: AWS secret.
        @param s3_dir: S3 staging directory.
        @param region: AWS Region.
        """

        if "s3://" not in s3_dir:
            raise Exception(f"s3_dir has received an invalid s3 path: {s3_dir}")

        logger.info("Creating instance of Datalake Client.")

        secrets_manager = hdxpyutils.SecretsManager()
        secret = secrets_manager.get_secret(secret_name)

        self.connection = connect(
            aws_access_key_id=secret["key"],
            aws_secret_access_key=secret["secret"],
            s3_staging_dir=s3_dir,
            region_name=region,
        )

    def query(self, sql_string: str):
        """Makes SQL query to Athena service.

        @param sql_string: SQL query.
        @returns pandas.DataFrame.
        """

        logger.info(f"Sending query to Athena. ({sql_string})")

        df = pd.read_sql(sql_string, self.connection)

        logger.info(f"Dataframe size: {df.size}")
        logger.info(f"Dataframe head:")
        logger.info(df.head(2))

        return df
