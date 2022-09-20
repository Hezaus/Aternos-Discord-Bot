import discord
import asyncio
from discord.ext import commands

import time

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
@commands.cooldown(1, 5, type=commands.BucketType.user)
async def StartServer(ctx):
    if servs._info:
        if servs._info['lang'] == 'online':
            await ctx.send('Server has already start on themincraftpros.aternos.me:45328')
        if servs._info['lang'] == 'loading':
            await ctx.send('Server is starting pls wait!')
        if servs._info['lang'] == 'offline':
            servs.start()
            await ctx.send('Server has started on themincraftpros.aternos.me:45328')

@StartServer.error
async def test_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
	    await ctx.send("Please try again after "f"{round(error.retry_after, 1)} seconds")

asyncio.run(socket.connect())

bot.run(TOKEN)