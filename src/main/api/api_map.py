from src.main.user.user_impl import *

API_MAP = {
    'user': {
        'GET': get_user,
        'POST': create_user,
        'DELETE': delete_user
    },
    'auth': {
        'register': {
            'POST': 'sample'
        },
        'login': {
            'GET': 'sample'
        }
    }
}
