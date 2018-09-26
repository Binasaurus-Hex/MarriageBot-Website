from flask import Flask,request, render_template,redirect,session
import requests
from user import User
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)
users = {}

'''
variables for oauth system
'''
redirect_uri = "http://127.0.0.1:5000/login"
scope = "identify%20guilds"
client_id = "468281173072805889"
client_secret = "ilP5Igpn-eXjWzilciBK02JdtkecCxDP"
authorization_url = "https://discordapp.com/oauth2/authorize?client_id="+client_id+"&redirect_uri="+redirect_uri+"&response_type=code&scope="+scope+""
discord_api_endpoint = "https://discordapp.com/api/oauth2/token"

'''

'''

'''
gets the token that can be exchanged for the 
user object from the discord api
'''
def get_token(code:str):

    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "scope": scope
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded" 
    }
    response = requests.post(discord_api_endpoint, data=payload, headers=headers)
    json_object = response.json()
    return json_object["access_token"]


'''
gets a user object of the user credentials
from a json object from discord
'''

def get_user_credentials(access_token:str):
    headers = {
        "Authorization" : f"Bearer {access_token}"
    }
    response_object = requests.post("http://discordapp.com/api/users/@me", headers=headers)
    user_json = response_object.json()
    user_object = User(user_json)
    return user_object

'''
redirects the user to the discord login page
'''
def oauth_login():
    return redirect(authorization_url)


'''
page the discord login redirects the user to
when successfully logged in with discord
'''
@app.route("/login",methods=['post','get'])
def login():
    code = request.args.get('code')
    if(code == None):
        return redirect("/")    
    token = get_token(code)
    user_object = get_user_credentials(token)
    session["user_token"] = token
    users[token] = user_object
    return redirect("/colours")

@app.route("/logout",methods=['get'])
def logout():
    del session["user_token"] 
    return redirect("/")    
    
@app.route("/colours",methods=["post","get"])
def colours():
    user_object = users.get(session["user_token"])
    return user_object.username

@app.route("/guilds",methods=["post","get"])
def guilds():
    pass

'''
main endpoint of the website
has "login with discord" button
if not logged in all pages should redirect here
'''
@app.route("/", methods=['get'])
def start():
    return render_template("login.html",marriagebot_logo = "http://hatton-garden.net/blog/wp-content/uploads/2012/03/wedding-rings.jpg",discord_oauth_url = authorization_url)
    

if(__name__ == "__main__"):
    app.run(debug=True)