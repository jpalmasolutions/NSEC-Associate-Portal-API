from src.main.utils.aws import existing_item,put_item_dynamo,delete_existing_item
from src.main.utils.logs import logger
import os

class User():

    ROLE_SET = ('ADMIN','CANVASSER','EXECUTIVE','SALES')
    TABLE = os.environ['NSEC_USER_TABLE']

    def __init__(self,body):
        if 'Email' in body:
            self.email = body['Email']
        else:
            logger.info('Email not present when initializing user.')
            raise Exception('Invalid user data.')

        self.password = ''
        self.role = ''
        self.first_name = ''
        self.last_name = ''
        self.number = ''

    '''
    def check_salesrabbit_user_exists
    '''

    def populate_user(self,body):
        if 'Password' in body:
            self.password = body['Password']
        else:
            logger.info('Password not present when initializing user.')
            raise Exception('Invalid user data.')

        if 'Role' in body:
            if body['Role'].upper() in self.ROLE_SET:
                self.role = body['Role']
            else:
                logger.info('Assigned role not in Role set.')
                raise Exception('Invalid user data.')
        else:
            self.role = ''

        self.first_name = '' if 'FirstName' not in body else body['FirstName']
        self.last_name = '' if 'LastName' not in body else body['LastName']
        self.number = '' if 'PhoneNumber' not in body else body['PhoneNumber']

    def user_exists(self):
        key = {
            'Email': self.email
            }

        return existing_item(key,self.TABLE)
    
    def add_user(self):
        item = {
            'Email': self.email,
            'FirstName': self.first_name,
            'LastName': self.last_name,
            'PhoneNumber': self.number,
            'Role': self.role,
            'Password': self.password
        }

        put_item_dynamo(item,self.TABLE)

    def delete_user(self):
        key = {
            'Email': self.email
        }

        delete_existing_item(key,self.TABLE)

    def return_user(self):
        return {
            'FirstName': self.first_name,
            'LastName': self.last_name,
            'Email': self.email,
            'PhoneNumber': self.number,
            'Role': self.role
        }