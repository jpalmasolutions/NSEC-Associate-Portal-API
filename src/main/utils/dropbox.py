import dropbox
from dropbox.sharing import SharedLinkSettings,RequestedLinkAccessLevel,LinkAudience
from dropbox.exceptions import ApiError
from requests.api import get
from src.main.utils.logs import logger
from src.main.utils.aws import get_secret

def dbx_upload(temp_path, upload_path):

    dropbox_secret = get_secret('dropbox')
    access_token = dropbox_secret.get('API_KEY')

    url = None

    with dropbox.Dropbox(oauth2_access_token=access_token) as dbx:
        with open(temp_path, 'rb') as body:
            try:
                dbx.files_get_metadata(upload_path)
                links = dbx.sharing_get_shared_links(upload_path)
                if len(links.links) > 0:
                    url = links.links[0].url
            except ApiError:
                logger.info('Uploading to Dropbox.')
                dbx.files_upload(body.read(),upload_path)
                setting = SharedLinkSettings(
                    require_password=False,
                    audience=LinkAudience.public,
                    allow_download=True,
                    access=RequestedLinkAccessLevel.viewer
                )
                response = dbx.sharing_create_shared_link_with_settings(upload_path,setting)
                url = response.url
    return url
