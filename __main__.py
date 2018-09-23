from flask import Flask,request, render_template,redirect
import requests
from user import User


app = Flask(__name__)
users = {}

redirect_uri = "http://127.0.0.1:5000/login"
scope = "identify%20guilds"
client_id = "468281173072805889"
client_secret = "ilP5Igpn-eXjWzilciBK02JdtkecCxDP"
authorization_url = "https://discordapp.com/oauth2/authorize?client_id="+client_id+"&redirect_uri="+redirect_uri+"&response_type=code&scope="+scope+""
discord_api_endpoint = "https://discordapp.com/api/oauth2/token"


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
    token = get_token(code)
    user_object = get_user_credentials(token)
    return str(user_object)
    


'''
main endpoint of the website
has "login with discord" button
if not logged in all pages should redirect here
'''
@app.route("/", methods=['post', 'get'])
def start():
    if(request.method == "POST"):
        if(request.form['login']):
            return oauth_login()
    elif(request.method == "GET"):
        return render_template("login.html",title_img = "https://cdn.discordapp.com/avatars/173147366818447361/d2904a8147f854cb334a75450a80e738.png?size=256")
    

if(__name__ == "__main__"):
    app.run(debug=True)