from ..settings import CONFIG_SETTINGS
import boto3

session = boto3.session.Session()

client = session.client(
    "s3",
    region_name=CONFIG_SETTINGS.REGION_NAME,
    endpoint_url=CONFIG_SETTINGS.ENDPOINT_URL,
    aws_access_key_id=CONFIG_SETTINGS.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=CONFIG_SETTINGS.AWS_SECRET_ACCESS_KEY,
)
