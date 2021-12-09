import json
from src.main.utils.logs import logger
from src.main.user.user_obj import User
from src.main.utils.utils import setup_response

def get_user(body):
    logger.info('From get user')
    response = setup_response()
    user = User(body)

    response_message = {}

    item = user.user_exists()

    if item:
        user.populate_user(item)
        response_message = user.return_user()
    else:
        response_message['ErrorMessage'] = 'User does not exist.'
        response['statusCode'] = 501

    response['body'] = json.dumps(response_message)
    return response

def delete_user(body):
    logger.info('From delete user')
    response = setup_response()
    user = User(body)

    response_message = {}

    if user.user_exists():
        user.delete_user()
        response_message['Message'] = 'User deleted.'
    else:
        response_message['Message'] = 'User does not exist.'

    response['body'] = json.dumps(response_message)

    return response