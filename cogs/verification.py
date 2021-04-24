from discord.ext import commands
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import random
import discord
import re


# user joins
# bot dms
# check if response contains @baruchmail.cuny.edu email (regex)
# if yes, send email with randomly generated code



class verification(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cache = {}

    # verification code generator
    def randomValue(self):
        return random.randint(100000, 999999)

    # cache to store an email / verification code 
    def cacheFunction(self, key, value):
        self.cache[key] = [value]

    # regex check on valid email
    def isBaruchEmail(self, email):
        regex = '^[_A-Za-z0-9-\\+]+\.+([_A-Za-z0-9-]+)*@baruchmail.cuny.edu$'
        if re.search(regex, email):
            return True
        return 0

    # message email with verification code
    def sendEmail(self, userEmail, vCode):
        message = Mail(
            from_email='frankdevacc@gmail.com',
            to_emails = userEmail,
            subject='Baruch AIS Verification Code - Expires in 30 minutes',
            html_content=str(vCode))
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e.message)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send_message('Please provide your @baruchmail.cuny.edu email for verification')


    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        if str(ctx.channel.type) == 'private':
            if self.isBaruchEmail(ctx.content):
                vCode = self.randomValue()
                self.cacheFunction(ctx.author, vCode)
                self.sendEmail(ctx.content, vCode)
                await ctx.channel.send('An Email has been sent, please be sure to check your spam folder.')
            else:
                await ctx.channel.send('Please provide a valid baruch student email.')
            

        


    
def setup(client):
    client.add_cog(verification(client))

