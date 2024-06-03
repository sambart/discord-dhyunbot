import asyncio
import contextlib
from sys import exception

import aiohttp
from pydis_core import BotBase
from pydis_core.utils.error_handling import handle_forbidden_from_block

from discord.errors import Forbidden
from discord.ext import commands as dpy_commands
from bot import constants, exts
import logging
from typing import (
    Optional,
)
import discord.ext.commands as commands
import discord
import inspect


log = logging.getLogger('bot')




class Bot(dpy_commands.bot.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=constants.Bot.prefix, case_insensitive=True)
        
        self._token = None
        self._session = None
        
    async def is_admin(self, member: discord.Member) -> bool:
        """Checks if a member is an admin of their guild."""
        try:
            for snowflake in await self._config.guild(member.guild).admin_role():
                if member.get_role(snowflake):
                    return True
        except AttributeError:  # someone passed a webhook to this
            pass
        return False

    async def add_cog(
        self,
        cog: commands.Cog,
        /,
        *,
        override: bool = False,
        guild: Optional[discord.abc.Snowflake] = discord.utils.MISSING,
        guilds: List[discord.abc.Snowflake] = discord.utils.MISSING,
    ) -> None:
        if not isinstance(cog, commands.Cog):
            raise RuntimeError(
                f"The {cog.__class__.__name__} cog in the {cog.__module__} package does "
                f"not inherit from the commands.Cog base class. The cog author must update "
                f"the cog to adhere to this requirement."
            )
        cog_name = cog.__cog_name__
        if cog_name in self.cogs:
            if not override:
                raise discord.ClientException(f"Cog named {cog_name!r} already loaded")
            await self.remove_cog(cog_name, guild=guild, guilds=guilds)

        if not hasattr(cog, "requires"):
            commands.Cog.__init__(cog)

        added_hooks = []

        try:
            for cls in inspect.getmro(cog.__class__):
                try:
                    hook = getattr(cog, f"_{cls.__name__}__permissions_hook")
                except AttributeError:
                    pass
                else:
                    self.add_permissions_hook(hook)
                    added_hooks.append(hook)

            await super().add_cog(cog, guild=guild, guilds=guilds)
            self.dispatch("cog_add", cog)
            if "permissions" not in self.extensions:
                cog.requires.ready_event.set()
        except Exception:
            for hook in added_hooks:
                try:
                    self.remove_permissions_hook(hook)
                except Exception:
                    # This shouldn't be possible
                    log.exception(
                        "A hook got extremely screwed up, "
                        "and could not be removed properly during another error in cog load."
                    )
            del cog
            raise

    def add_command(self, command: commands.Command, /) -> None:
        if not isinstance(command, commands.Command):
            raise RuntimeError("Commands must be instances of `redbot.core.commands.Command`")

        super().add_command(command)

        permissions_not_loaded = "permissions" not in self.extensions
        self.dispatch("command_add", command)
        if permissions_not_loaded:
            command.requires.ready_event.set()
        if isinstance(command, commands.Group):
            for subcommand in command.walk_commands():
                self.dispatch("command_add", subcommand)
                if permissions_not_loaded:
                    subcommand.requires.ready_event.set()
        if isinstance(command, (commands.HybridCommand, commands.HybridGroup)):
            command.app_command.extras = command.extras

    def remove_command(self, name: str, /) -> Optional[commands.Command]:
        command = super().remove_command(name)
        if command is None:
            return None
        command.requires.reset()
        if isinstance(command, commands.Group):
            for subcommand in command.walk_commands():
                subcommand.requires.reset()
        return command