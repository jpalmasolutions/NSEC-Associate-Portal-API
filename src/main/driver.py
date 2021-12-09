import json
from src.main.utils.logs import logger
from src.main.utils.event_request import Event_Request
from src.main.api.api_impl import serve_api_call
import traceback


def lambda_handler(event,context):

    '''
    This function is the entrypoint for the entire API.
    Receives:
    Event Object passed from API Gateway.
    Returns success/error HTTP Status based on event request.
    '''

    try:
        logger.info(json.dumps(event))
        #request context from API Gateway loaded into event object
        if 'requestContext' in event:
            event_request = Event_Request(event)
            return serve_api_call(event_request)
        else:
            raise Exception('Request Misconfigured.')

    except Exception as e:
        traceback.print_exc()

        response = {}
        response['statusCode'] = 500

        error_message = {}
        error_message['Message'] = 'Unknown error. Check logs.'

        response['body'] = json.dumps(error_message)
        
        return response


