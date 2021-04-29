from discord.ext import commands
import json
import os
import sys
import discord




class track(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.guildID = 0
        self.generalRole = 0
        self.analyticsRole = 0
        self.cyberRole = 0


    # retrieve tracks.json data, after parsing for major
    def getMajorRequirements(self, majorTrack):
        filename = os.path.dirname(os.getcwd())+"\\AIS-bot\\tracks.json"
        with open(filename) as tracks_json:
            data = json.load(tracks_json)
            return data[majorTrack]

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.client.guilds[0]
        self.generalRole = [role for role in self.guild.roles if role.name == 'General'][0]
        self.analyticsRole = [role for role in self.guild.roles if role.name == 'Data Analytics'][0]
        self.cyberRole = [role for role in self.guild.roles if role.name == 'Cyber'][0]


    @commands.command()
    async def track(self, ctx):
        if self.generalRole in ctx.author.roles:
            sendTrack = 'General'
            data = self.getMajorRequirements('General')
            majorReq = data["Required"]
            majorElec = data["Elective"]

        elif self.analyticsRole in ctx.author.roles:
            sendTrack = 'Data Analytics'
            data = self.getMajorRequirements('Data Analytics')
            majorReq = data["Required"]
            majorElec = data["Elective"]

        elif self.cyberRole in ctx.author.roles:
            sendTrack = 'Cyber'
            data = self.getMajorRequirements('Information Risk Management and Cybersecurity')
            majorReq = data["Required"]
            majorElec = data["Elective"]

        else:
            await ctx.send("You do not currently have any CIS major role. Please visit https://zicklin.baruch.cuny.edu/academic-programs/undergraduate/majors/computer-information-systems-cis-track/ to learn more")



        # generate the embeded message
        embedReqs = discord.Embed(
                color = discord.Colour.blue()
            )

        for key in majorReq:
            embedReqs.title = (f"Required - {sendTrack} Track")
            embedReqs.add_field(name=key, value=majorReq[key], inline=False)


        embedElec = discord.Embed(
                color = discord.Colour.blue()
            )
        
        for key in majorElec:
            embedElec.title = (f"Electives - {sendTrack} Track")
            embedElec.add_field(name=key, value=majorElec[key], inline=False)


        await ctx.send(embed=embedReqs)
        await ctx.send(embed=embedElec)
        

def setup(client):
    client.add_cog(track(client))
