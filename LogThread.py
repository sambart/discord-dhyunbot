
import discord
from discord import app_commands
from discord.ext import commands
import datetime

class ChannelMember:
    def __init__(self, user: discord.user):
        self.user:discord.user = user
        self.joined:datetime = datetime.datetime.now()
        self.outed:datetime = None
        self.last_message = None
        self.period = datetime.timedelta()
        self.state = 'in'
    
    def cal_period(self) -> datetime.timedelta:
        self.outed = datetime.datetime.now()
        self.period += self.outed - self.joined
        return self.period


    def __repr__(self):
        return f"<ChannelMember {self.user}>"

    def __str__(self):
        return f"{self.user.name}"
    
    def __eq__(self, other):
        return self.user == other.user
    
    
CATEGORY_BLACKLIST = [1139375856989511742]
CHANNEL_BLACKLIST = ['✔ㅣ채널생성']
    
class LogThread: 
    def __init__(self, thread: discord.Thread, voice_channel:discord.VoiceChannel):
        self.thread: discord.Thread = thread
        self.members = []
        self.joined = datetime.datetime.now()
        self.voice_channel:discord.VoiceChannel = voice_channel
        self.last_message = None
        self.create_member = None
        self.CATEGORY_BLACKLIST = [1139375856989511742]
        
        self.DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # def __repr__(self):
    #     return f"<LogThread {self.thread}>"
    
    # def __str__(self):
    #     return f"{self.thread.name}"
    
    # def __thread__(self):
    #     return self.thread
    
    async def send(self, message: str):
        await self.thread.send(message)
        
    @staticmethod
    async def create(noti_channel: discord.channel.ForumChannel, voice_channel: discord.VoiceChannel, member: discord.Member):
        if(voice_channel.category_id in CATEGORY_BLACKLIST):
            return None
        if(voice_channel.name in CHANNEL_BLACKLIST):
            return None
        sThread = (await noti_channel.create_thread(name=f"{voice_channel.name}", content=f'방생성 {member.display_name} [{datetime.datetime.now()}]')).thread
        lThread = LogThread(sThread, voice_channel)
        await lThread.enter_member(member)
        lThread.joined = datetime.datetime.now()
        lThread.create_member = member
        return lThread

    async def change_title(self, title: str):
        await self.thread.edit(name=title)
        
    async def enter_member(self, user: discord.user):
        if self.get_member(user) is None:            
            self.members.append(ChannelMember(user))
        self.get_member(user).joined = datetime.datetime.now()
            
        await self.send(f'[Bot]{user.display_name}님이 {self.voice_channel.name} 채널에 들어왔습니다!')
        
    async def leave_member(self, user: discord.user):
        if self.get_member(user) is None:
            return
        
        period = self.get_member(user).cal_period()
        total_hours = round(period.days * 24 + period.seconds / 3600, 2) #소수점 이하 2자리까지 반올림
        
        #self.members.remove(self.get_member(user))
        await self.send(f'[Bot]{user.display_name}님이 {self.voice_channel.name} 채널에서 나갔습니다!')
        await self.send(f'[Bot]{user.display_name}님이 {total_hours}시간동안 채널에 머물렀습니다!')
        
    def get_member(self, user: discord.user) -> ChannelMember:
        for member in self.members:
            if member.user == user:
                return member
        return None
    
    async def delete(self):
        self.outed = datetime.datetime.now()
        await self.send(f'[Bot] {self.voice_channel.name} 채널이 삭제되었습니다!')
        period = self.outed - self.joined
        total_hours = round(period.days * 24 + period.seconds / 3600, 2) #소수점 이하 2자리까지 반올림
        
        edit_message = f'```방이름: {self.voice_channel.name}\n - 생성자: {self.create_member.display_name}\n - 방생성시간: {self.joined.strftime(self.DATETIME_FORMAT)}\n - 방삭제시간: {self.outed.strftime(self.DATETIME_FORMAT)}\n - 방생존시간: {total_hours} \n\n - 방에 머문 멤버 목록\n'
        for member in self.members:
            period = member.period
            total_hours = round(period.days * 24 + period.seconds / 3600, 2) #소수점 이하 2자리까지 반올림
            edit_message += f'{member.user.display_name} : {total_hours}시간\n'
        edit_message += '```'
        await self.send(edit_message)
        #await self.thread.edit(name=f'{self.voice_channel.name}',)

    
    def __del__(self):
        self.delete()

