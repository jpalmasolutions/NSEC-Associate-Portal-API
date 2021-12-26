import json
import os
import requests
from src.main.utils.aws import get_secret
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
        calendly_api_key = get_secret('calendly')['API_KEY']
        headers = {}
        headers['Authorization'] = 'Bearer %s' % calendly_api_key
        headers['Content-Type'] = 'application/json'
        calendly_response = requests.get(calendly_body.get('event'),headers=headers)
        logger.info(calendly_response.text)


    response_message = {}

    response['body'] = json.dumps(response_message)

    return response

def salesrabbit_webhook(body):
    logger.info(json.dumps(body))
    response = {}

    if body.get('type') == 'form':
        leadId = body.get('leadId')
        url = "%s/leads/%s" % (os.environ['SALES_RABBIT_API'],leadId)
        rabbit_api_key = get_secret('salesrabbit')['API_KEY']
        headers = {}
        headers['authorization'] = 'Bearer %s' % rabbit_api_key
        lead_response = requests.get(url=url,headers=headers)
        lead_data = json.loads(lead_response.text).get('data')
        logger.info(lead_data)
        response = new(lead_data,True)
    else:
        response = setup_response()
        response_message = {}
        response['body'] = json.dumps(response_message)

    return response