import discord
from discord.ext import commands




class resources(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def resources(self, ctx):


        embedResources = discord.Embed(
                color = discord.Colour.blue()
            )
        embedResources.title = 'Resources'
        embedResources.add_field(name='Home Page', value='https://www.baruch.cuny.edu/', inline=False)
        embedResources.add_field(name='Baruch AIS Homepage', value='https://baruchais.com/', inline=False)
        embedResources.add_field(name='Baruch AIS LinkedIn', value='https://www.linkedin.com/company/baruchais/', inline=False)
        embedResources.add_field(name='Academic Calendar', value='https://enrollmentmanagement.baruch.cuny.edu/registrar/academic-calendar/', inline=False)
        embedResources.add_field(name='Department Directory Contacts', value='https://www.baruch.cuny.edu/directory/', inline=False)

        await ctx.send(embed=embedResources)


def setup(client):
    client.add_cog(resources(client))