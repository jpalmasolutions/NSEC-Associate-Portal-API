import boto3
from dynamodb_json import json_util as json
# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask, jsonify,render_template

def _get_items():

    session = boto3.session.Session(region_name='us-east-2',profile_name='junior')

    dynamodb = session.client(
            'dynamodb'
        )

    response = dynamodb.scan(
        TableName = 'nsec_leads',
    )

    items = response['Items']

    items = json.loads(items)

    return items
 
# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
 
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def get_items():
    items = _get_items()

    return jsonify(items)

@app.route('/chill.html')
def chill():
    return render_template('./chill.html')

@app.route('/list.html')
def serve_list():
    items = _get_items()
    return render_template('./list.html', content=items)

 
# main driver function
if __name__ == '__main__':
 
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True,host='0.0.0.0')
