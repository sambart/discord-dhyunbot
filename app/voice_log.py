
from discord.ext.commands import Cog, Context, command, has_any_role
from bot import Bot
import logging
import discord

log = logging.getLogger('bot')

class VoiceLog(Cog):

    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.threadDict: Dict[int, LogThread] = {}

    async def cog_load(self) -> None:
        return

    @Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState) -> None:
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

@Cog.listener
async def on_guild_channel_create(channel):
    now = datetime.now()
    pretty_time = now.strftime("%Y-%m-%d %H:%M:%S")
    
# 채널이 업데이트되었을 때 호출되는 이벤트
@Cog.listener
async def on_guild_channel_update(before, after):
    if before.name != after.name:
        change = f'채널 이름이 변경되었습니다: {before.name} -> {after.name}'
        print(change)
        if after.id in threadDict:
            thread: LogThread = threadDict[after.id]
            await thread.send(change)
            await thread.change_title(after.name)
            
    elif before.topic != after.topic:
        change = f'채널 주제가 변경되었습니다: {before.topic} -> {after.topic}'
    elif before.category != after.category:
        change = f'채널 카테고리가 변경되었습니다: {before.category} -> {after.category}'
    else:
        change = '채널이 업데이트되었습니다.'
        
# 채널이 삭제되었을 때 호출되는 이벤트
@Cog.listener
async def on_guild_channel_delete(channel):
    notification_channel_id = 1244054921502785656
    notification_channel = bot.get_channel(notification_channel_id)
    
    if notification_channel:        
        if channel.id in threadDict:
            await threadDict[channel.id].delete()
            del threadDict[channel.id]
            #await threadDict[channel.id].send(f'{channel.name} 채널이 삭제되었습니다.')


async def setup(bot: Bot) -> None:
    await bot.add_cog(VoiceGate(bot))
