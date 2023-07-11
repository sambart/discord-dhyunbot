import discord
from discord import app_commands
from discord.ext import commands

MY_GUILD = discord.Object(id=996054821100593273)
TOKEN = 'MTAzOTA3NTE2MjUzODExOTE3OA.GPQ9z5.Go7CZTYVotNoouj4oCwMlGmixvD6BkVlrTkM9k'

intents = discord.Intents.default()
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
        
class MemberRoles(commands.MemberConverter):
    async def convert(self, ctx, argument):
        member = await super().convert(ctx, argument)
        return [role.name for role in member.roles[1:]] # Remove everyone role!

@bot.tree.command(name='say')
@app_commands.describe(things_to_say = "뭐")
async def say(interaction: discord.Interaction, things_to_say: str):
    await interaction.response.send_message(f'{interaction.user.name} said: `{things_to_say}`')

@app_commands.context_menu()
async def react(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.send_message('Very cool message!', ephemeral=True)

    
@bot.tree.command(name='권한추가', description='testing')  # 명령어 이름, 설명
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"hey {ctx.author.name}, {user.name} has been giving a role called: {role.name}")

@bot.command(name="helpt", description="Returns all commands available")
async def help(ctx):
    helptext = "```"
    for command in self.bot.commands:
        helptext+=f"{command}\n"
    helptext+="```"
    await ctx.send(helptext)

bot.run(TOKEN)