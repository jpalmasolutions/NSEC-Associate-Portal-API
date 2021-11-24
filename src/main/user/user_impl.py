import json
from src.main.utils.logs import logger
from src.main.user.user_obj import User

def _setup_response():
    response = {}
    response['statusCode'] = 200
    response['body'] = None

    return response

def create_user(body):
    logger.info('From create user')
    response = _setup_response()
    user = User(body)
    response_message = {}

    if user.user_exists():
        response_message['Message'] = "User with email %s already exists" % user.email
    else:
        logger.info("Adding new user under email %s" % user.email)
        user.add_user()
        response_message['Message'] = 'User added.'

    response['body'] = json.dumps(response_message)

    return response

def get_user(body):
    logger.info('From get user')
    response = _setup_response()
    user = User(body)

    response_message = {}

    item = user.user_exists()

    if item:
        if user.check_user_credentials(item['Password']):
            response_message['Message'] = user.return_user()
        else:
            response_message['ErrorMessage'] = 'Username and Password do not match.'
            response['statusCode'] = 501
    else:
        response_message['ErrorMessage'] = 'Username and Password do not match.'
        response['statusCode'] = 501

    response['body'] = json.dumps(response_message)
    return response

def delete_user(body):
    logger.info('From delete user')
    response = _setup_response()
    user = User(body)

    response_message = {}

    if user.user_exists():
        logger.info('')
        user.delete_user()
        response_message['Message'] = 'User deleted.'
    else:
        response_message['Message'] = 'User does not exist.'

    response['body'] = json.dumps(response_message)

    return response

def validate_user_login(body):
    print(body)

def update_user_password(body):
    print(body)