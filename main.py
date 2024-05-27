import discord
import os
from discord import app_commands
from discord.ext import commands
import re
import dotenv
from datetime import datetime
import datetime
import copy

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
@bot.command(name='멤버역할부여')
@commands.has_permissions(manage_guild=True) #permissions
async def say(ctx):

    
    lv1_role = discord.utils.get(ctx.guild.roles, id=1040582879073284146)
    lv2_role = discord.utils.get(ctx.guild.roles, id=996077638298902528)
    lv3_role = discord.utils.get(ctx.guild.roles, id=1125037912317247528)
    lv4_role = discord.utils.get(ctx.guild.roles, id=1125038073340764170)

    print(lv1_role)
    print(lv2_role)
    print(lv3_role)
    print(lv4_role)
    #embed = discord.Embed(title='title', description='description', url='', color=discord.Color.random())

    i =0
    await ctx.send("역할 부여 시작")
    for member in ctx.guild.members:
        i +=1
        #print({member})
        join_days = datetime.datetime.now().astimezone() - member.joined_at
        if member.bot:
            continue
        #롤 지우기
        #  await member.remove_roles(lv1_role)
        #  await member.remove_roles(lv2_role)
        #  await member.remove_roles(lv3_role)
        #  await member.remove_roles(lv4_role)
        
        if join_days.days < 35:
            print("35일 이하")
            print({join_days.days}, {member.name}, {member.nick})
            if lv1_role in member.roles:
                continue

            if lv2_role in member.roles:
                await member.remove_roles(lv2_role)
            if lv3_role in member.roles:
                await member.remove_roles(lv3_role)
            if lv4_role in member.roles:
                await member.remove_roles(lv4_role)

            await member.add_roles(lv1_role)

        elif join_days.days < 180 and join_days.days >= 35:
            print("180일 이하")
            print({join_days.days}, {member.name}, {member.nick})
            
            if lv2_role in member.roles:
                continue

            if lv1_role in member.roles:
                await member.remove_roles(lv1_role)
            if lv3_role in member.roles:
                await member.remove_roles(lv3_role)
            if lv4_role in member.roles:
                await member.remove_roles(lv4_role)

            await member.add_roles(lv2_role)


        elif join_days.days < 365 and join_days.days >= 180:
            print("365일 이하")
            print({join_days.days}, {member.name}, {member.nick})

            if lv3_role in member.roles:
                continue

            if lv1_role in member.roles:
                await member.remove_roles(lv1_role)
            if lv2_role in member.roles:
                await member.remove_roles(lv2_role)
            if lv4_role in member.roles:
                await member.remove_roles(lv4_role)

            await member.add_roles(lv3_role)


        else:
            print("365일 이상")
            print({join_days.days}, {member.name}, {member.nick})

            if lv4_role in member.roles:
                continue

            if lv1_role in member.roles:
                await member.remove_roles(lv1_role)
            if lv2_role in member.roles:
                await member.remove_roles(lv2_role)
            if lv3_role in member.roles:
                await member.remove_roles(lv3_role)

            await member.add_roles(lv4_role)

    #embed.add_field(name='닉', value=member.nick, inline=True)
    await ctx.send("역할 부여 완료")
            #print({member.joined_at})
            #print({member.joined_at.strftime("%b %d, %Y, %T")})
            #data = f"{i};{member.name};{member.nick}"

@bot.command(name='온앤오프닉정규화')  # 명령어 이름, 설명
@commands.has_permissions(administrator=True) #permissions
async def say(ctx):
    embed = discord.Embed(title='title', description='description', color=discord.Color.random())

    p = re.compile('[abc]')
    i =0
    f = open("./onf_list.txt", 'w', encoding='utf-8')
    for guild in bot.guilds:
        for member in guild.members:
            if member.bot:
                continue
            join_days = datetime.datetime.now().astimezone() - member.joined_at
            if join_days.days < 35:
                continue
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

    await ctx.send(embed)

    
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