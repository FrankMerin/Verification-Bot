from discord.ext import commands
import discord

class on_join_trigger(commands.Cog):
    
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send('''**Welcome to the Baruch College Discord Server!**
    
    To gain access to the server, please visit #role-assignment channel and select a role.

    Additionally, to protect against spam, you must have an email attached to your discord account to talk in the server.

    **Optional:** If you would like to gain access to the verified students channel, please provide your @baruchmail.cuny.edu email for verification.''')

def setup(client):
    client.add_cog(on_join_trigger(client))