import json
from src.main.utils.logs import logger
from src.main.utils.utils import setup_response
from src.main.user.user_obj import User

def register(body):
    logger.info('From auth register')
    response = setup_response()
    user = User(body)
    user.populate_user(body)
    response_message = {}

    if user.user_exists():
        response['statusCode'] = 400
        response_message['Message'] = "User with email %s already exists" % user.email
    else:
        logger.info("Adding new user under email %s" % user.email)
        user.add_user()
        response_message['Message'] = 'User added.'

    response['body'] = json.dumps(response_message)

    return response


def login(body):
    logger.info('From auth login')
    response = setup_response()
    user = User(body)
    user.populate_user(body)
    item = user.user_exists()

    response_message = {}

    if item:
        if item['Password'] == user.password:
            user.populate_user(item)
            response_message = user.return_user()
        else:
            response_message['Message'] = 'Email and Password does not match.'
            response['statusCode'] = 401
    else:
        response_message['Message'] = 'User not found.'
        response['statusCode'] = 400

    response['body'] = json.dumps(response_message)

    return response