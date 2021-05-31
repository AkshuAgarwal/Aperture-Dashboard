import json

from quart import Quart, render_template, redirect, url_for
from quart_discord import DiscordOAuth2Session

app = Quart(__name__)

with open("./data/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

app.config["SECRET_KEY"] = config['secret_key']
app.config["DISCORD_CLIENT_ID"] = config['client_id']
app.config["DISCORD_CLIENT_SECRET"] = config['client_secret']
app.config["DISCORD_REDIRECT_URI"] = config['redirect_uri']

discord = DiscordOAuth2Session(app)

GUILD_INVITE_LINK = config['guild_invite_link']

@app.route("/")
async def home():
    return await render_template("index.html")

@app.route("/login")
async def login():
    return await discord.create_session(scope=['identify', 'guilds'])

@app.route("/callback")
async def callback():
    try:
        await discord.callback()
    except:
        return redirect(url_for("login"))

    return redirect(url_for("dashboard"))

@app.route("/invite")
async def invite():
    return await discord.create_session(scope=['identify', 'guilds', 'bot', 'applications.commands'], permissions=8)

@app.route("/support")
async def support():
    return redirect(GUILD_INVITE_LINK)

@app.route("/dashboard")
async def dashboard():
    user = await discord.fetch_user()
    return f"<h3>Success!</h3><h3>Logged in as {user.name}#{user.discriminator}</h3>"

if __name__ == '__main__':
    app.run(debug=True)