import discord
import asyncio
from discord.ext import commands

import os
from dotenv import load_dotenv

from python_aternos import Client, atwss

load_dotenv()

#Env stuff
TOKEN = os.getenv('TOKEN')
USER = os.getenv('USER')
PASS = os.getenv('PASS')

#Aternos stuff
aternos = Client.from_credentials(USER, PASS)

servs = aternos.list_servers()[0]

socket = servs.wss()

#Discord stuff
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned, intents=intents)

#bot events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

#socket stuff
@socket.wssreceiver(atwss.Streams.status)
async def status(info):
    servs._info = info

#commands
@bot.command()
async def StartServer(bot):
    if servs._info.lang == 'online' :
        await bot.send('Server has already start on themincraftpros.aternos.me:45328')
    elif servs._info.lang == 'loading' :
        await bot.send('Server is starting pls wait!')
    else:
        servs.start()
        await bot.send('Server has started on themincraftpros.aternos.me:45328')

asyncio.run(socket.connect())
bot.run(TOKEN)