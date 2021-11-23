import json
from src.main.utils.logs import logger
from src.main.utils.event_request import Event_Request
from src.main.api import serve_api_call
import traceback


def lambda_handler(event,context):

    '''
    This function is the entrypoint for the entire API.
    Receives:
    Event Object passed from API Gateway.
    Returns success/error HTTP Status based on event request.
    '''

    try:
        #request context from API Gateway loaded into event object
        if 'requestContext' in event:
            event_request = Event_Request(event)
            return serve_api_call(event_request)
        else:
            raise Exception('Request Misconfigured.')

    except KeyError as e:
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": {
                'ErrorMessage': 'Key Error. Check Logs.'
            }
        }
    except Exception as e:
        traceback.print_exc()
        return {
            "statusCode": 500,
            "body": {
                'ErrorMessage': 'Unexpected Error. Check Logs.'
            }
        }




