import json
from src.main.utils.aws import get_secret

class Event_Request:

    host = ""
    api_key = ""
    method = ""
    path = ""
    body = None

    def _validate_api_key(self):
        api_key = get_secret('nsec-associate-portal-api')

        if not api_key['API-KEY'] == self.api_key:
            raise Exception('BAD API KEY')

    def _validate_host(self):
        if not self.host == 'api.nsec-associate.com':
            raise Exception('HOST ERROR')



    def __init__(self,event):
        self.host = event['requestContext']['domainName']
        self._validate_host()
        self.api_key = event['requestContext']['identity']['apiKey']
        self._validate_api_key()
        self.method = event['requestContext']['httpMethod']
        self.path = event['requestContext']['path']
        self.body = json.loads(event['body'])