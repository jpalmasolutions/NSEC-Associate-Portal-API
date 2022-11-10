import logging
import os
from flask import Flask, jsonify
from src.service.lead import lead_bp
from werkzeug.exceptions import (BadRequest, HTTPException,
                                 InternalServerError, MethodNotAllowed,
                                 NotFound)


def configure_logging():
    # register root logging
    logging.basicConfig(level=logging.INFO)
    logging.getLogger(__name__).setLevel(logging.INFO)

app = Flask(__name__)

@app.errorhandler(InternalServerError)
@app.errorhandler(NotFound)
@app.errorhandler(BadRequest)
@app.errorhandler(MethodNotAllowed)
def server_error(error : HTTPException):

    app.logger.error(error.description)
    payload = {
        'error': error.description
    }

    status = 500 if error.code == None else error.code

    return jsonify(payload), status

if __name__ == "__main__":
    configure_logging()
    app.register_blueprint(lead_bp)
    app.run(
        debug=bool(os.environ.get('DEBUG',False))
    )
