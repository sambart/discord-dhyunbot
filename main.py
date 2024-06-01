import discord
import os
from discord import app_commands
from discord.ext import commands
import re
import dotenv
from datetime import datetime
import copy
from LogThread import LogThread
from typing import Dict

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

threadDict: Dict[int, LogThread] = {}

@bot.event
async def on_ready():
    print("")
    try:
        synced = await bot.tree.sync()
        print(f"synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

@bot.event
async def on_voice_state_update(member : discord.Member, before : discord.VoiceState, after : discord.VoiceState):
    now = datetime.now()
    pretty_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # 특정 텍스트 채널 ID로 설정합니다.
    notification_channel_id = 1244054921502785656
    notification_channel = bot.get_channel(notification_channel_id)

    # 사용자가 음성 채널에 들어갔을 때
    if after.channel is not None and before.channel is None:
        if notification_channel:
            if after.channel.id in threadDict:
                lThread = threadDict[after.channel.id]
                await lThread.enter_member(member)
            else:
                lThread = await LogThread.create(notification_channel, after.channel, member)
                if lThread:
                    threadDict[after.channel.id] = lThread
                
        print(f'{member.display_name}님이 {after.channel.name} 채널에 들어왔습니다!')

    # 사용자가 음성 채널에서 나갔을 때
    elif before.channel is not None and after.channel is None:
        if notification_channel:
            if before.channel.id in threadDict:
                lThread = threadDict[before.channel.id]
                await lThread.leave_member(member)
                    
        print(f'{member.display_name}님이 {before.channel.name} 채널에서 나갔습니다.')

    # 사용자가 한 음성 채널에서 다른 음성 채널로 이동했을 때
    elif before.channel is not None and after.channel is not None:        
        if before.channel.id == after.channel.id:
            return
        
        if notification_channel:
            if before.channel.id in threadDict:               
                lThread = threadDict[before.channel.id]              
                await lThread.leave_member(member)
                                    
            if after.channel.id in threadDict:
                lThread = threadDict[after.channel.id]
                await lThread.enter_member(member)
                
            else:
                lThread = await LogThread.create(notification_channel, after.channel, member)
                if lThread:
                    threadDict[after.channel.id] = lThread
                
        print(f'{member.display_name}님이 {before.channel.name} 채널에서 {after.channel.name} 채널로 이동했습니다.')

bot.run(TOKEN)
