from src.main.utils.aws import existing_item,put_item_dynamo
from src.main.utils.password import check_password,hash_password
from src.main.utils.logs import logger

class User():
    first_name = ""
    last_name = ""
    email = ""
    number = ""
    rabbit_user_id = ""
    role = ""
    password = ""

    def __init__(self,body):
        self.first_name = body['FirstName']
        self.last_name = body['LastName']
        self.email = body['Email']
        self.number = body['PhoneNumber']
        self.role = body['Role']
        self.password = body['Password']

    '''
    def check_salesrabbit_user_exists
    '''

    def user_exists(self):
        key = {
            'Email': self.email,
            'FirstName': self.first_name
        }

        return existing_item(key)
    
    def add_user(self):
        hashed_password = hash_password(self.password)
        item = {
            'Email': self.email,
            'FirstName': self.first_name,
            'LastName': self.last_name,
            'PhoneNumber': self.number,
            'Role': self.role,
            'Password': hashed_password
        }

        put_item_dynamo(item)

    def check_user_credentials(self,password):
        return check_password(self.password,password.value)

    def return_user(self):
        return {
            'FirstName': self.first_name,
            'LastName': self.last_name,
            'Email': self.email,
            'PhoneNumber': self.number,
            'Role': self.role
        }