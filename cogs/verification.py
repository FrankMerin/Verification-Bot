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


discordTag = (os.environ.get('DiscordTag'))


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

    #check if user is blocked for attempting more then 3 emails.
    def isBlocked(self, ctx):
        if ctx.author.id not in self.cache:
            return False
        return self.cache[ctx.author.id][2] > 3

    # cache to store an email / verification code get guild roles
    def cacheFunction(self, user_id, verification_code, email, usedEmails, numberOfAttempts):
        self.cache[user_id] = [verification_code, email, 0, 0]
    

    # regex check on valid email
    def isBaruchEmail(self, email):
        regex = '^.*@baruchmail\.cuny\.edu$'
        if re.search(regex, email, re.IGNORECASE):
            return True
        return 0

    # convert user object to member object    
    def getMember(self, user):
        return self.guild.get_member(user)
    

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
            from_email='discord.baruch@gmail.com',
            to_emails = userEmail,
            subject='Baruch College Discord Verification Code',
            html_content=str(vCode))
        try:
            sg = SendGridAPIClient(os.environ.get('BaruchCollegeMailKey'))
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)


    @commands.command()
    async def verify(self, ctx):
        if self.verified_role in self.getMember(ctx.author.id).roles:
            return await ctx.author.send(f"You are already verified. If this is not true, please message {discordTag}.")
        await ctx.author.send("If you would like to gain access to the verified students channel, please provide your @baruchmail.cuny.edu email to recieve a verification code.")

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.client.guilds[0]
        self.verified_role = [role for role in self.guild.roles if role.name == 'Verified'][0]
        self.verified_channel = [channel for channel in self.guild.channels if channel.name == 'verification-log'][0]

   
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return
        if ctx.content.startswith('!'):
            return
        if str(ctx.channel.type) == 'private' and self.verified_role in self.getMember(ctx.author.id).roles:
            return await ctx.channel.send(f"You are already verified. If this is not true, please message {discordTag}.")
        if str(ctx.channel.type) == 'private' and self.isBlocked(ctx):
            await ctx.channel.send(f"You have been blocked for too many attempts. Please try again in 1-2 days or message {discordTag}.")
            return
        if str(ctx.channel.type) == 'private':
            if self.isBaruchEmail(ctx.content):      
                # updates email provided attempt
                vCode = self.randomValue()
                if ctx.author.id not in self.cache:
                    self.cacheFunction(ctx.author.id, vCode, ctx.content, 0, 0)
                else:
                    self.cache[ctx.author.id][0] = vCode
                self.cache[ctx.author.id][2] += 1
                self.sendEmail(ctx.content, vCode)     
                await ctx.channel.send('A verification code has been sent to your Email, please be sure to check your spam folder and provide the verification code.')

            elif self.isCode(ctx.content) and ctx.author.id in self.cache:
                user_code = int(ctx.content)                
                if self.cache[ctx.author.id][0] == user_code:
                    member = await self.guild.fetch_member(ctx.author.id)
                    # add roles incase user is new joiner, custom to server due to interaction with other bots
                    if self.guild.get_role(657803668719927297) in member.roles:
                        await member.add_roles(self.guild.get_role(482611413504884746))
                        await member.remove_roles(self.guild.get_role(657803668719927297))
                    await member.add_roles(self.verified_role)
                    await ctx.channel.send("Successfully verified")
                    await self.verified_channel.send(f'User {ctx.author} was verified with {self.cache[ctx.author.id][1]}')
                    self.cache.pop(ctx.author.id)
                else: 
                    await ctx.channel.send("Code Invalid")
                    if self.cache[ctx.author.id][3] >= 5:
                        self.cache[ctx.author.id][2] += 1
                        await ctx.channel.send('Too many invalid codes, please provide a valid Baruch Email to try again.')
                    self.cache[ctx.author.id][3] += 1
            else:
                await ctx.channel.send('Please provide a valid baruch student email.')
            

def setup(client):
    client.add_cog(verification(client))