import os
import pathlib

import requests
from flask import url_for
from flask import Flask, session, abort, redirect, render_template, request
# from flask_session import Session
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
from yaml import SafeLoader, load


with open('config.yaml','r') as config_yaml:
    config = load(config_yaml,SafeLoader)

app = Flask("Google Login App")
app.config['SECRET_KEY'] = 'SOME_SECRET'
# app.config["SESSION_PERMANENT"] = False
# app.config["SESSION_TYPE"] = "filesystem"
# Session(app)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = config['google_oauth_client']
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    print("print 1st @ login")
    print( session)
    print(" ")



    return redirect( authorization_url)
    



@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)
    

    if 'state' not in session or session["state"] != request.args["state"]:
        print("print 2nd @ callback")
        print( session)
        print(" ")
        abort(500)  # State does not match!

    print("3st callback")
    print( session)
    print(" ")
  
    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
  
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    
    return redirect("/")


@app.route("/logout")
def logout():
    session["google_id"] = ""
    session["name"] = ""
    session["email"] = ""
    session.pop('username', None)
    session.clear()
    return redirect("/")


is_session_empty = False

@app.route("/")
def index():

    client = {
            "google_id": "",
            "name": "",
            "email": "",
            "current": ""

            }
   
    print(session)
    if not session.get('email'):
        client["current"] = "index"
        print('Not logged in.')
    elif session.get('email'):
        client = {
            "google_id": session["google_id"],
            "name": session["name"],
            "email": session["email"],
            "current": "index"
            }

    return render_template('./index.html', client = client)

@app.route("/about")
def about():

    client = {
            "google_id": "",
            "name": "",
            "email": "",
            "current": ""
            }
   
    print(session)
    if not session.get('email'):
        client["current"]  = "about"
        print('Not logged in.')
    elif session.get('email'):
        client = {
            "google_id": session["google_id"],
            "name": session["name"],
            "email": session["email"],
            "current": "about"
            }

    return render_template('./about.html', client = client)



@app.route("/profile")
@login_is_required
def protected_area():


    client = {
            "google_id": session["google_id"],
            "name": session["name"],
            "email": session["email"],
            "current": "profile"

            }

    return render_template('./profile.html', client = client)
    #return f"Hello {session['name']}! <br/> <a href='/logout'><button>Logout</button></a>"

@app.route("/tools")
def tool():
   

    client = {
            "google_id": "",
            "name": "",
            "email": "",
            "current": ""
            }
    
    if not session.get('email'):
        return redirect('../')
        print('Not logged in.')
    elif session.get('email'):
        
        client["google_id"] = session["google_id"]
        client["name"] = session["name"]
        client["email"] = session["email"]
        client["current"] = "tools"
        
        return render_template('./tools.html', client = client)
    
@app.route("/form")
def form():
    client = {
                "google_id": "",
                "name": "",
                "email": "",
                "current": ""
                }
        
    if not session.get('email'):
        return redirect('../')
        print('Not logged in.')
    elif session.get('email'):
        
        client["google_id"] = session["google_id"]
        client["name"] = session["name"]
        client["email"] = session["email"]
        client["current"] = "form"
        
        return render_template('./form.html', client = client)
    

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')