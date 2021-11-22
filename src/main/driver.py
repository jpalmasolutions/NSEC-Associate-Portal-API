from src.main.utils.logs import logger

def lambda_handler(event,context):

    logger.info(event)