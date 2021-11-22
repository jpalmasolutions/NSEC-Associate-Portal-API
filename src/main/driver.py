import json
from src.main.utils.logs import logger

def lambda_handler(event,context):

    logger.info(event)

    return {
        "statusCode": 404,
        "body": json.dumps('Cheers from AWS Lambda!!')
    }