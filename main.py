# Imports

import discord 
from discord.ext import commands 
import sqlite3
import json 
from init_database import init_prefix_db
import random 

# Initialising our database
init_prefix_db()


# Grabbing data from our config file
def get_token():
    with open("config.json", "r") as f:
        data = json.load(f)
        return data["token"]


def get_default_prefix():
    with open("config.json", "r") as f:
        data = json.load(f)
        return data["base_prefix"]


# Prefix function declaration and client declaration
def get_prefix(client, message : discord.Message):
    conn = sqlite3.connect("prefix.db")
    c = conn.cursor()
    with conn:
        c.execute("""SELECT * FROM prefix_data WHERE id = :id""", {"id" : message.guild.id})
        data = c.fetchone()
        return data[1]

client = commands.Bot(command_prefix=get_prefix)

# on_ready event
@client.event 
async def on_ready():
    print(f"{client.user} has now logged in with the ID {client.user.id}!")



# Prefix command and it's error handling
@client.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx : commands.Context, *, prefix : str):
    conn = sqlite3.connect("prefix.db")
    c = conn.cursor()
    with conn:
        c.execute("""UPDATE prefix_data SET prefix = :prefix WHERE id = :id""", {"prefix" : prefix, "id" : ctx.guild.id})
        await ctx.send(f"Successfully changed prefix to {prefix}")


@prefix.error 
async def prefix_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f".prefix <prefix>")

    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You need admin for this command to work, {ctx.author.mention}!")


# on_guild_join event 


@client.event 
async def on_guild_join(guild : discord.Guild):
    conn = sqlite3.connect("prefix.db")
    c = conn.cursor()
    with conn:
        c.execute("""INSERT INTO prefix_data VALUES (:id, :prefix)""", {'id' : guild.id, "prefix" : get_default_prefix()})
        await random.choice(guild.text_channels.send(f"Thank you for inviting me to your server! My prefix is {get_default_prefix()}!"))


# Running the bot
client.run(get_token())