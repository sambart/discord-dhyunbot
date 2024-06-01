import discord
import os
from discord import app_commands
from discord.ext import commands
import re
import dotenv
from datetime import datetime
import datetime


bot.instance = Bot(
    guild_id=constants.Guild.id,
    http_session=session,
    redis_session=await _create_redis_session(),
    statsd_url=statsd_url,
    command_prefix=commands.when_mentioned_or(constants.Bot.prefix),
    activity=discord.Game(name=f"Commands: {constants.Bot.prefix}help"),
    case_insensitive=True,
    max_messages=10_000,
    allowed_mentions=discord.AllowedMentions(everyone=False, roles=allowed_roles),
    intents=intents,
    allowed_roles=list({discord.Object(id_) for id_ in constants.MODERATION_ROLES}),
)
await bot.start
