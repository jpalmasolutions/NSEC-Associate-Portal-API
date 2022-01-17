import json
import os
import requests
from src.main.utils.aws import get_secret
from src.main.lead.lead_impl import new,update
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
    response = setup_response()
    response_message = {}

    if body.get('type') == 'form':

        #get lead ID from form submission data
        leadId = body.get('leadId')

        #Call SalesRabbit API to get full Lead Details
        url = "%s/leads/%s" % (os.environ['SALES_RABBIT_API'],leadId)

        #Get Salesrabbit API Key from secrets manager
        rabbit_api_key = get_secret('salesrabbit')['API_KEY']
        headers = {}
        headers['authorization'] = 'Bearer %s' % rabbit_api_key

        #Call API and get Payload
        lead_response = requests.get(url=url,headers=headers)
        lead_data = json.loads(lead_response.text).get('data')

        logger.info(json.dumps(lead_data))

        #Based on which form was submitted, either need to update lead or add new lead
        form_data = body.get('formData')
        form_id = body.get('formId')
        form_data['canvasser'] = body.get('leadMetaData').get('owner')

        if form_id == 8:
            if form_data.get('sendLead',False):
                response = new(lead_data | form_data,True)
        elif form_id == 9:
            response = update(lead_data | form_data,True)
        else:
            logger.info('Form not handled.')
    else:
        response['body'] = json.dumps(response_message)

    return response