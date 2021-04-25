import random
import discord
import os
import asyncio
import re
from discord.ext import commands
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# user joins
# bot dms

# NEW - on message filter for args*
# -- if the passed arg matches email format, follow email path
# -- if the passed arg is 8 digits, check library 

# ALTERNATIVE: send the passcode as "!AIS 12345678" and create a command that reacts to !AIS, 
# this way we dont need to filter on message

# NEW - can update the value in dictionary to contain array with email address & verification code



# check if response contains @baruchmail.cuny.edu email (regex)
# if yes, send email with randomly generated code






class verification(commands.Cog):
    

    def __init__(self, client):
        self.client = client
        self.cache = {}

    guildID = 280776371779928074
    channelID = 684929894768967726
    roleID = 835621668931108954


    # verification code generator
    def randomValue(self):
        return random.randint(10000000, 99999999)

    # cache to store an email / verification code 
    def cacheFunction(self, key, value, email):
        self.cache[key] = [value, email]

    # regex check on valid email
    def isBaruchEmail(self, email):
        regex = '^[_A-Za-z0-9-\\+]+\.+([_A-Za-z0-9-]+)*@baruchmail.cuny.edu$'
        if re.search(regex, email):
            return True
        return 0
    
    def isCode(self, code):
        print(code)
        try:
            int(code)
            return True
        except Exception:
            return False

    def checkCode(self, msg):
        return str(self.cache[msg.author.id]).strip('[]') == str(msg.content)

    def checkCode(self, msg):
        return self.cache[msg.author.id] == msg.content

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
            print(e.message)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.send('Please provide your @baruchmail.cuny.edu email for verification')


    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return

        #determine what is the content if number between the range of verification codes, its vercode
        # if its e

        
        
        originalCTX = ctx # re-assignment of context variable due to on_message reseting ctx from bot messages
        if str(originalCTX.channel.type) == 'private':
            if self.isBaruchEmail(originalCTX.content):
                vCode = self.randomValue()
                self.cacheFunction(originalCTX.author.id, vCode, originalCTX.content)
                self.sendEmail(originalCTX.content, vCode)
                print(self.cache)
                await originalCTX.channel.send('An Email has been sent, please be sure to check your spam folder.')
            elif self.isCode(originalCTX.content):
                user_code = int(originalCTX.content)
                if self.cache[originalCTX.author.id][0] == user_code:
                    guild = await self.client.fetch_guild(280776371779928074)
                    role = guild.get_role(835621668931108954)
                    channel = self.client.get_channel(684929894768967726)
                    member = await guild.fetch_member(originalCTX.author.id)
                    await member.add_roles(role)
                    await originalCTX.channel.send("Successfully verified")
                    await channel.send(f'User {originalCTX.author} was verified with {self.cache[originalCTX.author.id][1]}')              
            else:
                await ctx.channel.send('Please provide a valid baruch student email.')
            

        


    
def setup(client):
    client.add_cog(verification(client))

