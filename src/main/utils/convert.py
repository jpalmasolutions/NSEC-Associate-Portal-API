import convertapi
from src.main.utils.logs import logger
from src.main.utils.aws import get_secret

def to_jpg(file,from_format):
    convert_api_secrets = get_secret('convertapi')
    convertapi.api_secret = convert_api_secrets.get('API_SECRET')
    response = convertapi.convert('jpg',{
        'File': file
    },from_format)

    file = response.save_files('/tmp/')

    return file.pop()