import convertapi
from src.main.utils.logs import logger

def to_jpg(file,from_format):
    convertapi.api_secret = 'OnkqZVfpaslkavWn'
    response = convertapi.convert('jpg',{
        'File': file
    },from_format)

    file = response.save_files('/tmp/')

    return file.pop()