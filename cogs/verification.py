from discord.ext import commands
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import random
import discord
import re
import asyncio




# Messages users on join
# check if private message response contains @baruchmail.cuny.edu email (regex)
# if yes, send email with randomly generated code
# waits for response with a code
# if code valid, assign verified role



class verification(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        self.cache = {}
        self.guild = 0
        self.verified_role = 0
        self.verified_channel = 0


    # verification code generator
    def randomValue(self):
        return random.randint(10000000, 99999999)

    # cache to store an email / verification code get guild roles
    def cacheFunction(self, user_id, verification_code, email):
        self.cache[user_id] = [verification_code, email]

    # regex check on valid email
    def isBaruchEmail(self, email):
        regex = '^[_A-Za-z0-9-\\+]+\.+([_A-Za-z0-9-]+)*@baruchmail.cuny.edu$'
        if re.search(regex, email):
            return True
        return 0
    
    #check if the message being sent is a message
    def isCode(self, code):
        print(code)
        try:
            int(code)
            return True
        except Exception:
            return False

    # validates if the code assigned to the userID is 
    def checkCode(self, msg):
        return str(self.cache[msg.author.id]).strip('[]') == str(msg.content)

    # check if the message is a verification code
    def isCode(self, code):
        try:
            int(code)
            return True
        except Exception:
            return False

    # check if user provided code matches the real code
    def checkCode(self, msg):
        return str(self.cache[msg.author.id]).strip('[]') == str(msg.content)

    # message email with verification code
    def sendEmail(self, userEmail, vCode):
        message = Mail(
            from_email='frankdevacc@gmail.com',
            to_emails = userEmail,
            subject='Baruch AIS Verification Code - Expires in 30 minutes',
            html_content=str(vCode))
        try:
            sg = SendGridAPIClient(os.environ.get('AISmailKey'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.client.guilds[0]
        self.verified_role = [role for role in self.guild.roles if role.name == 'verified'][0]
        self.verified_channel = [channel for channel in self.guild.channels if channel.name == 'verified'][0]

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send('Please provide your @baruchmail.cuny.edu email for verification')

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        if ctx.content.startswith('!'):
            return
        if str(ctx.channel.type) == 'private':
            if self.isBaruchEmail(ctx.content):
                vCode = self.randomValue()
                self.cacheFunction(ctx.author.id, vCode, ctx.content)
                self.sendEmail(ctx.content, vCode)
                await ctx.channel.send('An Email has been sent, please be sure to check your spam folder.')
            elif self.isCode(ctx.content):
                user_code = int(ctx.content)                
                if self.cache[ctx.author.id][0] == user_code:
                    member = await self.guild.fetch_member(ctx.author.id)
                    await member.add_roles(self.verified_role)
                    await ctx.channel.send("Successfully verified")
                    await self.verified_channel.send(f'User {ctx.author} was verified with {self.cache[ctx.author.id][1]}')
                else: 
                    await ctx.channel.send("Code Invalid")
            else:
                await ctx.channel.send('Please provide a valid baruch student email.')
            

def setup(client):
    client.add_cog(verification(client))

