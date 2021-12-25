from src.main.utils.aws import put_item_dynamo,existing_item
import os

class Lead():

    TABLE = os.environ['NSEC_LEAD_TABLE']

    def _validate_lead(self):
        for key in self.data:
            if not self.data.get(key):
                raise Exception('Lead details not fully provided.')

    def __init__(self,body,from_rabbit):
        self.data = {}
        if from_rabbit:
            self.data['Street'] = body.pop('street1')
            self.data['City'] = body.pop('city')
            self.data['State'] = body.pop('state')
            self.data['FirstName'] = body.pop('firstName')
            self.data['LastName'] = body.pop('lastName')
            self._validate_lead()
            self.data['PostalCode'] = body.pop('postalCode','')
            self.data['EmailAddress'] = body.pop('email','')
            self.data['PhoneNumber'] = body.pop('primaryPhone','')
            self.data['Notes'] = body.pop('notes','')
            self.data['RabbitLeadId'] = body.pop('leadId',None)
            self.data['Appointment'] = None
            

        else:
            self.data['Street'] = body.pop('StreetName')
            self.data['City'] = body.pop('City')
            self.data['State'] = body.pop('State')
            self.data['FirstName'] = body.pop('FirstName')
            self.data['LastName'] = body.pop('LastName')
            self._validate_lead()
            self.data['PostalCode'] = body.pop('PostalCode','')
            self.data['EmailAddress'] = body.pop('EmailAddress','')
            self.data['PhoneNumber'] = body.pop('PhoneNumber','')
            self.data['Notes'] = body.pop('Notes','')
            self.data['Appointment'] = None

        # self.data['Other'] = body

        street = self.data['Street'].replace(' ','').lower().strip()
        city = self.data['City'].lower()
        state = self.data['State'].upper()
        first_name = self.data['FirstName'].lower()
        last_name = self.data['LastName'].lower()


        self.lead_id = '%s.%s.%s.%s.%s' % (first_name,last_name,street,city,state)


    def lead_exists(self):
        key = {
            'ID': self.lead_id
        }

        return existing_item(key,self.TABLE)

    def add_lead(self):
        item = {
            'ID': self.lead_id,
            'Data': self.data
        }

        put_item_dynamo(item,self.TABLE)
