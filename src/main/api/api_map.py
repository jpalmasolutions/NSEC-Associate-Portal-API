from src.main.user.user_impl import *
from src.main.auth.auth_impl import *
from src.main.lead.lead_impl import *
from src.main.utils.webhooks import *

API_MAP = {
    'api': {
        'user': {
            'GET': get_user,
            'DELETE': delete_user
        },
        'auth': {
            'register': {
                'POST': register
            },
            'login': {
                'POST': login
            }
        },
        'lead': {
            'new': {
                'POST': new
            },
            's3': {
                'POST': exit,
                'PUT': exit
            }
        }
    },
    'calendly': {
        'POST': calendly_webhook
    },
    'salesrabbit': {
        'POST': salesrabbit_webhook
    }
}
