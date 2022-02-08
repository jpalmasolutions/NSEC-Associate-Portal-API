from src.main.utils.aws import put_item_dynamo,existing_item,get_secret,upload_to_s3,update_item_dynamo
from src.main.utils.convert import to_jpg
from src.main.utils.dropbox import dbx_upload
from src.main.utils.logs import logger
from datetime import datetime
import os
import requests

class Lead():

    TABLE = os.environ['NSEC_LEAD_TABLE']

    def _validate_lead(self):
        for key in self.data:
            if not self.data.get(key):
                raise Exception('Lead details not fully provided.')

    def _get_rabbit_files(self,files):
        try:
            file_dict = {}
            for file in files:
                logger.info(file)
                url = "%s/leads/%s/files/%s" % (os.environ['SALES_RABBIT_API'],self.data['RabbitLeadId'],file['fileId'])
                rabbit_api_key = get_secret('salesrabbit')['API_KEY']
                headers = {}
                headers['authorization'] = 'Bearer %s' % rabbit_api_key
                file_name = file['fileName']
                mime = file_name.split('.')[-1].lower()

                lead_response = requests.get(url=url,headers=headers)
                tmp_path = '/tmp/%s' % file_name

                with open(tmp_path,'wb+') as file_byte:
                    file_byte.write(lead_response.content)
                    file_byte.close()

                if mime != 'jpg' and mime != 'png':
                    if mime == 'heic':
                        tmp_path = to_jpg(tmp_path,mime)
                        file_name = tmp_path.split('/')[-1]
                    else:
                        raise Exception('Mime type %s is not supported.' % (mime))

                upload_path = 'salesrabbit/%s/%s' % (self.data['RabbitLeadId'], file_name)
                logger.info('Uploading %s' % file_name)
                s3_path = upload_to_s3(tmp_path,upload_path)
                dbx_path = dbx_upload(tmp_path,'/%s' % upload_path)
                file_dict[file_name] = {}
                file_dict[file_name]['s3'] = s3_path
                file_dict[file_name]['dbx'] = dbx_path

                os.remove(tmp_path)

            return file_dict
        except Exception as e:
            logger.info(e)
            logger.info('Could not download files for salesrabbit lead id %s' % self.data['RabbitLeadId'])
            return {}

    def __init__(self,body,from_rabbit):
        self.data = {}
        if from_rabbit:
            self.data['Street'] = body.get('street1')
            self.data['City'] = body.get('city')
            self.data['State'] = body.get('state')
            self.data['PostalCode'] = body.get('zip')
            self.data['RabbitLeadId'] = str(body.get('id')).strip()
            self._validate_lead()
            self.data['Suite'] = body.get('street2','')

        else:
            self.data['Street'] = body.get('StreetName')
            self.data['City'] = body.get('City')
            self.data['State'] = body.get('State')

        street = self.data['Street'].replace(' ','.').lower().strip()
        suite = self.data['Suite'].replace(' ','.').lower().strip()
        street_addr = '{street}{suite}'.format(street=street,suite=suite)
        city = self.data['City'].lower()
        state = self.data['State'].upper()
        zip = self.data['PostalCode']
        rabbit = '0' if not self.data.get('RabbitLeadId') else self.data.get('RabbitLeadId')


        self.lead_id = '{street}.{city}.{state}.{zip}.{rabbit}'.format(street=street_addr,city=city,state=state,zip=zip,rabbit=rabbit)

    def populate_full_lead(self,body,from_rabbit):
        if from_rabbit:
            self.data['FirstName'] = body.get('firstName').strip()
            self.data['LastName'] = body.get('lastName').strip()
            self.data['PostalCode'] = body.get('zip','').strip()
            self.data['EmailAddress'] = body.get('email','').strip()
            self.data['PhoneNumber'] = body.get('phonePrimary','').strip()
            self.data['Notes'] = '' if not body.get('notes') else body.get('notes').strip()
            self.data['Appointment'] = '' if not body.get('appointment') else body.get('appointment').strip()
            self.data['Canvasser'] = body.get('canvasser','').strip()
            custom_fields = body.get('customFields') if isinstance(body.get('customFields'),dict) else {}
            self.data['SalesRep'] = custom_fields.get('salesRep','').strip()
            self.data['LeadType'] = custom_fields.get('typeOfLead','').strip()
            self.data['Files'] = self._get_rabbit_files(body.get('files',[]))
            self.data['Status'] = body.get('status','').strip()
        else:
            self.data['PostalCode'] = body.get('PostalCode','')
            self.data['EmailAddress'] = body.get('EmailAddress','')
            self.data['PhoneNumber'] = body.get('PhoneNumber','')
            self.data['Notes'] = body.get('Notes','')
            self.data['Appointment'] = None

        self.created_at = datetime.strftime(datetime.now(),'%m-%d-%Y-%H:%M:%S%f')
    
    def lead_exists(self):
        key = {
            'ID': self.lead_id
        }

        return existing_item(key,self.TABLE)

    def add_lead(self):
        item = {
            'ID': self.lead_id,
            'Data': self.data,
            'CreatedAt': self.created_at
        }

        put_item_dynamo(item,self.TABLE)


    def update_lead(self):
        key = {
            'ID': self.lead_id
        }

        update_expr = "set #d=:d"

        expr_attr_val = {
            ':d': self.data
        }

        expr_attr_names = {
            '#d': 'Data'
        }

        update_item_dynamo(key,update_expr,expr_attr_val,expr_attr_names,self.TABLE)

