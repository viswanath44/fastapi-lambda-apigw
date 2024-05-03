import json
from botocore.exceptions import ClientError


class ConfigParser:

    def __init__(self, session):
        self.ssm_client = session.client("ssm")

    def load_config(self, parameter_name: str):
        try:
            response = self.ssm_client.get_parameter(
                Name=parameter_name, WithDecryption=True
            )
            config_json = response["Parameter"]["Value"]
            # Validate and return the configuration {"key":"xxxxxxxxxxxx"}
            return json.loads(config_json)["key"]
        except ClientError as e:
            raise Exception(f"Failed to fetch parameter: {e}")
