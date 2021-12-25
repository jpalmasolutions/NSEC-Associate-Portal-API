import json
from src.main.utils.aws import get_secret


class Event_Request:

    def _validate_host(self):
        if not self.host == 'api.nsec-associate.com':
            raise Exception('HOST ERROR')

    def __init__(self, event):
        self.host = event['requestContext']['domainName']
        self._validate_host()
        self.method = event['requestContext']['httpMethod']
        self.path = event['requestContext']['path']
        self.body = json.loads(event['body'])
