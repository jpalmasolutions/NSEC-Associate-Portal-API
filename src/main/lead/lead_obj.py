from src.main.utils.aws import put_item_dynamo,existing_item,get_secret,upload_to_s3
from src.main.utils.logs import logger
import os
import requests
from PIL import Image
import pyheif

class Lead():

    TABLE = os.environ['NSEC_LEAD_TABLE']

    def _validate_lead(self):
        for key in self.data:
            if not self.data.get(key):
                raise Exception('Lead details not fully provided.')

    def _get_rabbit_files(self,files):
        try:
            for file in files:
                logger.info(file)
                url = "%s/leads/%s/files/%s" % (os.environ['SALES_RABBIT_API'],self.data['RabbitLeadId'],file['fileId'])
                rabbit_api_key = get_secret('salesrabbit')['API_KEY']
                headers = {}
                headers['authorization'] = 'Bearer %s' % rabbit_api_key
                lead_response = requests.get(url=url,headers=headers)
                heif_file = pyheif.read(lead_response.content)
                image = Image.frombytes(
                    heif_file.mode, 
                    heif_file.size, 
                    heif_file.data,
                    "raw",
                    heif_file.mode,
                    heif_file.stride,
                    )
                image.save('test.jpg', 'JPEG')
                file_name = 'test.jpg'
                upload_to_s3(file_name)
                
        except Exception as e:
            logger.info('Could not download files for salesrabbit lead id %s' % self.data['RabbitLeadId'])
        finally:
            return {}

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
            self.data['RabbitLeadId'] = body.pop('leadId','')
            self.data['Appointment'] = None
            self.data['Files'] = self._get_rabbit_files(body.pop('files'))
            

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
