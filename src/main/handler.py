import serverless_wsgi
from src.main import driver
from src.service.lead import lead_bp

#Hanlde Flask Application Via Serverless Invocation
def lambda_handler(event, context):
    driver.configure_logging()
    driver.app.register_blueprint(lead_bp)
    return serverless_wsgi.handle_request(driver.app, event, context)
