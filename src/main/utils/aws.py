import boto3
import base64
from botocore.exceptions import ClientError
import json
import os
from src.main.utils.logs import logger


def get_secret(secret_name):
    region_name = os.environ['REGION']

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)
        else:
            decoded_binary_secret = base64.b64decode(
                get_secret_value_response['SecretBinary'])
            return decoded_binary_secret


def _get_table(table_name):
    dynamodb = boto3.resource('dynamodb', region_name=os.environ['REGION'])
    table = dynamodb.Table(table_name)
    return table


def put_item_dynamo(item, table):

    table = _get_table(table)

    table.put_item(
        Item=item
    )


def update_item_dynamo(key, update_expr, expr_attr_val, expr_attr_names, table):
    table = _get_table(table)
    table.update_item(
        Key=key,
        UpdateExpression=update_expr,
        ExpressionAttributeValues=expr_attr_val,
        ExpressionAttributeNames=expr_attr_names
    )


def delete_existing_item(key, table):
    table = _get_table(table)

    table.delete_item(
        Key=key
    )


def existing_item(key, table):
    table = _get_table(table)
    item = table.get_item(
        Key=key
    )

    if "Item" in item:
        return item['Item']
    else:
        return None

def _key_existing_size__head(client, bucket, key):
    """return the key's size if it exist, else None"""
    try:
        obj = client.head_object(Bucket=bucket, Key=key)
        return obj.get('ContentLength')
    except ClientError as exc:
        if exc.response['Error']['Code'] != '404':
            raise

def upload_to_s3(temp_path, object_path):
    session = boto3.Session()
    s3_client = session.client('s3')
    bucket = os.environ['BUCKET']

    size = _key_existing_size__head(s3_client,bucket,object_path)
    size_file = os.path.getsize(temp_path)

    with open(temp_path, 'rb') as body:
        if not size or size != size_file:
            logger.info('Uploading to S3.')
            s3_client.put_object(
                Body=body,
                Bucket=bucket,
                Key=object_path
            )

    return 's3://%s/%s' % (bucket, object_path)


def trigger_sns_topic(arn, message):

    sns_client = boto3.client('sns')

    sns_client.publish(
        TargetArn=arn,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )
