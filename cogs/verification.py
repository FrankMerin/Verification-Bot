import random
import discord
import os
import asyncio
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

    # verification code generator
    def randomValue(self):
        return random.randint(10000000, 99999999)

    # cache to store an email / verification code 
    def cacheFunction(self, key, value):
        self.cache[key] = [value]

    # regex check on valid email
    def isBaruchEmail(self, email):
        regex = '^[_A-Za-z0-9-\\+]+\.+([_A-Za-z0-9-]+)*@baruchmail.cuny.edu$'
        if re.search(regex, email):
            return True
        return 0

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
            sg = SendGridAPIClient(os.environ('AISmailKey'))
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
                self.cacheFunction(ctx.author.id, vCode)
                self.sendEmail(ctx.content, vCode)
                await ctx.channel.send('An Email has been sent, please be sure to check your spam folder.')
            
                try:
                    msg = await self.client.wait_for('message', check=self.check)
                except asyncio.TimeoutError:
                    await ctx.channel.send('Invalid verification code')
                else:
                    role = discord.utils.get(ctx.author.guild.roles, name='verified')
                    await ctx.author.add_roles(role)
                    await ctx.channel.send("Successfully verified")

            else:
                await ctx.channel.send('Please provide a valid baruch student email.')
            

        


    
def setup(client):
    client.add_cog(verification(client))

