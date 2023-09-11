import discord
import os
from discord import app_commands
from discord.ext import commands
import re
import dotenv
from datetime import datetime
import datetime

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
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
TOKEN = os.environ["TOKEN"]

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

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    print(payload)
    channel = bot.get_channel(1140192448056922152)
    role = discord.utils.get(payload.member.guild.roles, name="관전자")
    #member = payload.member
    guild = bot.get_guild(payload.guild_id)
    member: discord.Member = payload.member
    if payload.channel_id != channel.id:
        return
    if payload.emoji.name == "✅":  
        if " ㄱ" not in member.nick:  
            newNick = member.nick + " ㄱ"
            await member.edit(nick = newNick)
        #if role in member.roles:
        #    await member.remove_roles(role) #removes the role if user already has
        #else:
        #    newNick = member.nick + " ㄱ"
        #    print(member)
        #    await member.add_roles(role)
        #    await member.edit(nick = newNick)


@bot.event
async def on_raw_reaction_remove(payload: discord.RawReactionActionEvent):
    print(payload)
    guild = bot.get_guild(payload.guild_id)
    member = discord.utils.get(guild.members, id=payload.user_id)
    channel = bot.get_channel(1140192448056922152)
    role = discord.utils.get(member.guild.roles, name="관전자")

    if payload.channel_id != channel.id:
        return
    if payload.emoji.name == "✅":  
        print(role)
        #if member.nick in " ㄱ":            
        newNick = member.nick.rstrip(" ㄱ")
        await member.edit(nick = newNick)
            
        #if role in member.roles:
         #   newNick = member.nick.rstrip(" ㄱ")
         #   await member.edit(nick = newNick)
         #   await member.remove_roles(role) #removes the role if user already has


#관전용 이모지
@bot.command(name='관전이모지')
@commands.has_permissions(administrator=True) #permissions
async def say(ctx):
    channel = bot.get_channel(1140192448056922152)
    text= "관전을 하시려면 이모지를 클릭해 닉네임을 변경해주세요. 봇이 꺼져있을때는 작동 안할 수 있습니다."
    Moji = await channel.send(text)
    await Moji.add_reaction('✅')
    #await channel.connect()
    
#뉴비 멤버 변경
@bot.command(name='뉴비')
@commands.has_permissions(administrator=True) #permissions
async def say(ctx):
    i =0
    for guild in bot.guilds:
        for member in guild.members:
            i +=1
            print({member})
            now = datetime.datetime.now() + datetime.timedelta(days=30)
            print({})
            print({member.joined_at})
            print({member.joined_at.strftime("%b %d, %Y, %T")})
            print({member.name}, {member.nick})
            data = f"{i};{member.name};{member.nick}"

@bot.command(name='온앤오프닉정규화')  # 명령어 이름, 설명
@commands.has_permissions(administrator=True) #permissions
async def say(ctx):
    embed = discord.Embed(title='title', description='description', url='', color=discord.Color.random())


    p = re.compile('[abc]')
    i =0
    f = open("./onf_list.txt", 'w', encoding='utf-8')
    for guild in bot.guilds:
        for member in guild.members:
            i +=1
            print({i})
            print({member.name}, {member.nick})
            data = f"{i};{member.name};{member.nick}"
            #data = i, " - ", member.name, " ", member.nick
            print(data)
            f.write(data)
            f.write("\n")

            #strMemeber += member.nick
            embed.add_field(name='닉', value=member.nick, inline=True)

    f.close()


    await ctx.send(embed=embed)

    
@bot.tree.command(name='권한테스트', description='testing')  # 명령어 이름, 설명
@commands.has_permissions(administrator=True) #permissions
#@app_commands.describe()
async def giverole(ctx, user: discord.Member, role: discord.Role):
    #const guild = client.guilds.cache.get('Guild ID') 
    await user.add_roles(role)

@bot.command(name="helpt", description="Returns all commands available")
@commands.has_permissions(administrator=True) #permissions
async def help(ctx):
    helptext = "```"
    for command in self.bot.commands:
        helptext+=f"{command}\n"
    helptext+="```"
    await ctx.send(helptext)

bot.run(TOKEN)