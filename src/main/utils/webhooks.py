import json
import requests
from src.main.lead.lead_impl import new
from src.main.utils.logs import logger
from src.main.utils.utils import setup_response

def calendly_webhook(body):
    logger.info(json.dumps(body))
    response = setup_response()

    if body.get('event') == 'invitee.created':
        calendly_body = body.get('payload')
        name = calendly_body.get('name')
        name = name.split(' ')
        first_name = name[0]
        last_name = name[1:]

        headers = {}
        headers['Authorization'] = 'Bearer %s' % ''
        headers['Content-Type'] = 'application/json'
        calendly_response = requests.get(calendly_body.get('event'),headers=headers)
        logger.info(calendly_response.text)


    response_message = {}

    response['body'] = json.dumps(response_message)

    return response

def salesrabbit_webhook(body):
    logger.info(json.dumps(body))
    response = {}

    if body.get('eventType') == 'leadCreate':
        response = new(body.get('leadData'),True)
    else:
        response = setup_response()
        response_message = {}
        response['body'] = json.dumps(response_message)

    return response