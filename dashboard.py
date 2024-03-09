import os
from quart import Quart, render_template, redirect, url_for
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from discord.ext import ipc
import discord
from config import *

app = Quart(__name__) #

app.secret_key = b"news.gg"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

app.config["DISCORD_CLIENT_ID"] = 1161632275147014226
app.config["DISCORD_CLIENT_SECRET"] = "9porZKZyCoidSI6erKV5-voMHljiTi6b"
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_BOT_TOKEN"] = "MTE2MTYzMjI3NTE0NzAxNDIyNg.GIdZE3.5PJWsYh_r6j3Bzx6nbjh8Re6ZpfsCQs6lY_FRs"

discord = DiscordOAuth2Session(app)

@app.route("/login/")
async def login():
    return await discord.create_session()


@app.route("/callback/")
async def callback():
    try:
        await discord.callback()
    except:
        return redirect(url_for("login"))
    
    return redirect(url_for("dashboard"))

@app.route("/")
async def index():
    return await render_template("index.html")


@app.route("/dashboard/")
async def dashboard():
    user = await discord.fetch_user()
    return await render_template("dashboard.html", user=user)



if __name__ == "__main__":
    app.run(debug=True)