import json
from src.main.utils.logs import logger

def lambda_handler(event,context):

    try:

        logger.info(event)

    except Exception as e:
        return {
            "statusCode": 404,
            "body": json.dumps('Error in Lambda')
        }
    else:
        return {
            "statusCode": 200,
            "body": json.dumps('Cheers from AWS Lambda!!')
        }