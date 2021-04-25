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

        embed.title = 'Bot Commands'
        embed.description = "Message AIS Bot directly with an Email to receive a verification code. Providing AIS Bot the verification code will grant you the verified role in Discord."
        embed.add_field(name='!track', value='Returns Major class requirements for you active CIS Track', inline=False)
        embed.add_field(name='!resources', value='Returns useful Baruch resource links', inline=False)
        await ctx.author.send(embed=embed)


    


def setup(client):
    client.add_cog(help(client))