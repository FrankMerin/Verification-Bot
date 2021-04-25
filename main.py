import re
import discord
from discord.ext import commands
import os


intents = discord.Intents.default()
intents.members = True

discord_key = (os.environ.get('CCbot-API2'))
client = commands.Bot(command_prefix='!', intents=intents)
client.remove_command('help')



@client.command()
async def load(ctx, extention):
    client.load_extension(f'cogs.{extention}')


if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in os.listdir("cogs") if os.path.isfile(os.path.join("cogs", f))]:
        try:
            client.load_extension("cogs" + "." + extension)
        except Exception as e:
            print(f'Failed to load extension {extension}.')
            print(e)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="!help"))


client.run(discord_key, bot=True, reconnect=True)