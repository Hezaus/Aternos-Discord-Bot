import discord
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content == 'ping':
            await message.channel.send('pong')

intents = discord.Intents.default()
intents.message_content = True
bot = MyClient(intents=intents)
command = commands.Bot(command_prefix='>', intents=intents)

@command.command()
async def ping(ctx):
    await ctx.send('safdasfsafsa')

TOKEN = os.getenv('TOKEN')

bot.run(TOKEN)