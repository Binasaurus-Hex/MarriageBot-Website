from flask import Flask,request, render_template,redirect,session
import requests
from user import User
import os
from oauth import Oauth
from marriagebot import Marriagebot


app = Flask(__name__)
app.secret_key = os.urandom(24)
users = {}
oauth = Oauth()

'''
page the discord login redirects the user to
when successfully logged in with discord
'''
@app.route("/login",methods=['post','get'])
def login():
    code = request.args.get('code')
    if(code == None):
        return redirect("/")

    token = oauth.get_token(code)
    user_object = oauth.get_user_credentials(token)
    session["user_token"] = token
    users[token] = user_object
    return redirect("/colours")

@app.route("/submit_colours",methods=['post','get'])
def submit_colours():
    colours = request.form
    user_object = users.get(session.get("user_token"))

    Marriagebot.set_colours(user_id = user_object.id,
                            edge = colours["edge_colour"].strip('#'),
                            node = colours["node_colour"].strip('#'),
                            font = colours["font_colour"].strip('#'),
                            highlighted_font = colours["highlighted_font_colour"].strip('#'),
                            highlighted_node = colours["highlighted_node_colour"].strip('#'),
                            background = colours["background_colour"].strip('#'))
    return redirect("/colours")

@app.route("/submit_prefix/<guild_id>",methods=['post'])
def submit_prefix(guild_id):
    prefix = request.form.get("prefix")
    user_object = users.get(session.get("user_token"))
    guild_object = user_object.get_guild(guild_id)
    guild_object.prefix = prefix
    Marriagebot.set_prefix(guild_id = guild_object.id,
                            prefix = prefix,
                            user_id = user_object.id)
    return redirect("/guilds/"+guild_id)

'''
page that logs the user out
'''
@app.route("/logout",methods=['get'])
def logout():
    del session["user_token"] 
    return redirect("/")    

'''
page that allows user to select colours and submit them
'''
@app.route("/colours",methods=["post","get"])
def colours():
    if(session.get("user_token") == None):
        return redirect("/")
    else:
        
        user_object = users.get(session.get("user_token"))
        colours = Marriagebot.get_colours(user_object.id)
        guild_list = user_object.guild_list
        print(colours["edge"])
        return render_template("colours.html",
                                colours_url = "/colours",
                                guilds_url = "/guilds",
                                logout_url = "/logout",
                                user_avatar = user_object.get_avatar_url(),
                                username = user_object.get_name(),
                                marriagebot_logo = "http://hatton-garden.net/blog/wp-content/uploads/2012/03/wedding-rings.jpg",
                                edge_colour = colours["edge"],
                                node_colour = colours["node"],
                                font_colour = colours["font"],
                                highlighted_font_colour = colours["highlighted_font"],
                                highlighted_node_colour = colours["highlighted_node"],
                                background_colour = colours["background"],
                                guild_list = guild_list
                                )

'''
page that allows user to select guild out of guilds they own
and select the bot prefix and submit it
'''
@app.route("/guilds",methods=["post","get"])
def guilds():
    if(session.get("user_token") == None):
        return redirect("/")
    else:
        user_object = users.get(session.get("user_token"))
        guilds = user_object.guild_list
        return redirect("/guilds/"+guilds[0].id)


@app.route("/guilds/<guild_id>",methods=["get"])
def selected_guild(guild_id):
    if(session.get("user_token") == None):
        return redirect("/")
    else:
        user_object = users.get(session.get("user_token"))
        guild_list = user_object.guild_list
        selected_guild = user_object.get_guild(guild_id)

        return render_template("guilds.html",
                                colours_url = "/colours",
                                guilds_url = "/guilds",
                                logout_url = "/logout",
                                user_avatar = user_object.get_avatar_url(),
                                username = user_object.get_name(),
                                marriagebot_logo = "http://hatton-garden.net/blog/wp-content/uploads/2012/03/wedding-rings.jpg",
                                guild_list = guild_list,
                                selected_guild = selected_guild)

'''
main endpoint of the website
has "login with discord" button
if not logged in all pages should redirect here
'''
@app.route("/", methods=['get'])
def start():
    return render_template("login.html",
                            marriagebot_logo = "http://hatton-garden.net/blog/wp-content/uploads/2012/03/wedding-rings.jpg",
                            discord_oauth_url = oauth.authorization_url)

    

if(__name__ == "__main__"):
    app.run('0.0.0.0', debug=True)