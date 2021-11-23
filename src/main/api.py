from src.main.user.user_impl import *
from src.main.utils.event_request import Event_Request
from src.main.utils.logs import logger

API_MAP = {
    'user': {
        'GET': get_user,
        'POST': create_user,
        'DELETE': delete_user
    }
}

def _check_in_api_map(event_request:Event_Request):
    paths = event_request.path.split('/')[1:]
    method = event_request.method

    curr = API_MAP

    for path in paths:
        if not path in curr:
            raise Exception('Path does not exist.')
        else:
            curr = curr[path]

    if not method in curr:
        raise Exception('%s does not serve method %s' % (event_request.path,method))
    
    return curr[method]

def serve_api_call(event_request:Event_Request):
     func_call = _check_in_api_map(event_request)

     return func_call(event_request.body)