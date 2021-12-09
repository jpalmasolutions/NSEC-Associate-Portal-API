from src.main.utils.utils import setup_response
from src.main.lead.lead_obj import Lead
import json
from src.main.utils.logs import logger

def new(body):

    response = setup_response()
    respones_message = {}
    lead = Lead(body)

    if lead.lead_exists():
        response['statusCode'] = 400
        respones_message['Message'] = 'Lead already exists.'
        raise Exception('Lead alredy exists.')
    else:
        logger.info('Adding lead %s.' % lead.lead_id)
        lead.add_lead()
        respones_message['Message'] = 'Lead added.'
    
    response['body'] = json.dumps(respones_message)
    return response
