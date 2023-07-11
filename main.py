import discord
import os
from discord import app_commands
from discord.ext import commands
import re

#설치파일 확인
try:
    import nacl
except ImportError:
    try:
        if os.name == 'nt':
            os.system("py -m pip install pynacl")
        else:
            os.system("python3 -m install pynacl")
    except Exception as e:
        print("Error:", e)
        exit()

MY_GUILD = discord.Object(id=996054821100593273)
TOKEN = 'MTAzOTA3NTE2MjUzODExOTE3OA.GPQ9z5.Go7CZTYVotNoouj4oCwMlGmixvD6BkVlrTkM9k'

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print("")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.command(name='테스트1')
async def say(ctx):
    channel = ctx.author.voice.channel

    for guild in bot.guilds:
        for member in guild.members:
            print({member})

    await ctx.send(f"command test: {channel}")
    await channel.connect()
    
    
@bot.command(name='온앤오프닉정규화')  # 명령어 이름, 설명
async def say(ctx):
    embed = discord.Embed(title='title', description='description', url='', color=discord.Color.random())


    p = re.compile('[abc]')
    
    for guild in bot.guilds:
        for member in guild.members:
            print({member})

            #strMemeber += member.nick
            embed.add_field(name='닉', value=member.nick, inline=True)
    await ctx.send(embed=embed)

    
@bot.tree.command(name='권한테스트', description='testing')  # 명령어 이름, 설명
#@app_commands.describe()
async def giverole(ctx, user: discord.Member, role: discord.Role):
    #const guild = client.guilds.cache.get('Guild ID') 
    await user.add_roles(role)

@bot.command(name="helpt", description="Returns all commands available")
async def help(ctx):
    helptext = "```"
    for command in self.bot.commands:
        helptext+=f"{command}\n"
    helptext+="```"
    await ctx.send(helptext)

bot.run(TOKEN)