from src.main.utils.aws import put_item_dynamo,existing_item
import os

class Lead():

    TABLE = os.environ['NSEC_LEAD_TABLE']

    def __init__(self,body):
        self.street = body['StreetName']
        self.city = body['City']
        self.state = body['State']
        self.postal_code = body['PostalCode']
        self.first_name = body['FirstName']
        self.last_name = body['LastName']
        self.number = body['PhoneNumber']
        self.email = body['EmailAddress']

        street = self.street.replace(' ','').lower().strip()
        city = self.city.lower()
        state = self.state.upper()
        first_name = self.first_name.lower()
        last_name = self.last_name.lower()


        self.lead_id = '%s.%s.%s.%s.%s' % (first_name,last_name,street,city,state)

    def _generate_lead_data(self):
        return {
            "StreetName": self.street,
            "City": self.city,
            "State": self.state,
            "ZipCode": self.postal_code,
            "FirstName": self.first_name,
            "LastName": self.last_name,
            "EmailAddress": self.email,
            "PhoneNumber": self.number
        }

    def lead_exists(self):
        key = {
            'ID': self.lead_id
        }

        return existing_item(key,self.TABLE)

    def add_lead(self):
        data = self._generate_lead_data()

        item = {
            'ID': self.lead_id,
            'Data': data
        }

        put_item_dynamo(item,self.TABLE)
