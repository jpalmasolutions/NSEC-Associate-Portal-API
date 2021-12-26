from src.main.utils.utils import setup_response
from src.main.lead.lead_obj import Lead
from src.main.utils.aws import trigger_sns_topic
import json
import os
from src.main.utils.logs import logger

def new(body,salesrabbit=False):

    response = setup_response()
    respones_message = {}
    lead = Lead(body,salesrabbit)

    if lead.lead_exists():
        response['statusCode'] = 400
        respones_message['Message'] = 'Lead already exists.'
    else:
        logger.info('Adding lead %s.' % lead.lead_id)
        lead.add_lead()
        respones_message['Message'] = 'Lead added.'
        sns_message = {
            'Key': lead.lead_id
        }
        trigger_sns_topic(os.environ['NSEC_PUBLISHER_SNS_ARN'],sns_message)
    
    response['body'] = json.dumps(respones_message)
    return response

def file_upload(body):
    response = setup_response()
    respones_message = {}

    file_type = body['FileType']
    file_name = body['FileName']