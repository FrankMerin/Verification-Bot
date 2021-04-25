import discord
from discord.ext import commands


class help(commands.Cog):

    def __init__(self, client):
        self.client = client


    # help information
    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.green()
        )

        embed.set_author(name='Bot Commands')
        embed.add_field(name='!AC', value='Returns Major class requirements for you active CIS Track', inline=False)
        await ctx.author.send(embed=embed)


    


def setup(client):
    client.add_cog(HelpFunction(client))