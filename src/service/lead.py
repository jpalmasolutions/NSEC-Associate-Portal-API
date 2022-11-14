import jsons
from datetime import datetime

from flask import Blueprint, jsonify, make_response, request
from flask_api import status
from src.models.lead import Lead
from src.dto.lead import LeadDTO
from src.utils.constants import DEFAULT_GET_LIMIT, DEFAULT_GET_OFFSET

lead_bp = Blueprint('lead',__name__,url_prefix='/api')

@lead_bp.route('/leads', methods = ['POST'])
def add_lead():
    body = request.json

    lead_inst = jsons.load(json_obj = body, cls = Lead)
    lead_dto = LeadDTO()

    row = lead_dto.find_lead(lead = lead_inst)

    if row:
        payload = {
            'lead_id': row[0]
        }
        return make_response(jsonify(payload),status.HTTP_200_OK)
    else:
        lead_inst.assign_id()
        lead_dto.insert_lead(lead = lead_inst)

    print(lead_inst.json)

    return make_response(jsonify(lead_inst),status.HTTP_201_CREATED)

@lead_bp.route('/leads', methods = ['GET'])
def get_all_leads():
    lead_dto = LeadDTO()

    query_params = request.args
    
    limit = query_params.get('limit',default = DEFAULT_GET_LIMIT, type = int)
    limit = limit if limit <= DEFAULT_GET_LIMIT else DEFAULT_GET_LIMIT
    offset = query_params.get('offset', default = DEFAULT_GET_OFFSET, type = int)

    leads = lead_dto.get_all_leads(limit = limit, offset = offset)

    return make_response(jsonify(leads),status.HTTP_200_OK)

@lead_bp.route('/leads/<id>', methods = ['GET'])
def get_lead(id : str):
    lead_dto = LeadDTO()
    status_code = status.HTTP_200_OK
    payload = {}
    lead = lead_dto.get_lead(lead_id=id)

    if lead == None:
        status_code = status.HTTP_404_NOT_FOUND
    else:
        payload = lead.json

    return make_response(jsonify(payload),status_code)

@lead_bp.route('/leads/<id>', methods = ['DELETE'])
def delete_lead(id : str):

    lead_dto = LeadDTO()

    lead_dto.delete_lead(lead_id = id)

    return make_response(jsonify({}),status.HTTP_204_NO_CONTENT)