from discord.ext import commands
import json
from pathlib import Path
import os
import sys
import discord




class track(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.guildID = 280776371779928074
        self.generalRoleID = 835916642504015892
        self.analyticsRoleID = 835916806610747393
        self.cyberRoleID = 835916902345343017


    # retrieve tracks.json data, after parsing for major
    def getMajorRequirements(self, majorTrack):
        filename = os.path.dirname(os.getcwd())+"\\AIS-bot\\tracks.json"
        with open(filename) as tracks_json:
            data = json.load(tracks_json)
            return data[majorTrack]

    
    @commands.command()
    async def track(self, ctx):
        guild = await self.client.fetch_guild(self.guildID)
        generalRole = guild.get_role(self.generalRoleID)
        analyticsRole = guild.get_role(self.analyticsRoleID)
        cyberRole = guild.get_role(self.cyberRoleID)

        if generalRole in ctx.author.roles:
            sendTrack = 'General'
            data = self.getMajorRequirements('General')
            majorReq = data["Required"]
            majorElec = data["Elective"]

        elif analyticsRole in ctx.author.roles:
            sendTrack = 'Data Analytics'
            data = self.getMajorRequirements('Data Analytics')
            majorReq = data["Required"]
            majorElec = data["Elective"]

        elif cyberRole in ctx.author.roles:
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
