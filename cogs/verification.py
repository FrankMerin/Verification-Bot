from discord.ext import commands


class verification(commands.Cog):

    def __init__(self, client):
        self.client = client

    # stuff goes here 
    
def setup(client):
    client.add_cog(verification(client))