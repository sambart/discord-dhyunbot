import discord
import os
from discord import app_commands
from discord.ext import commands
import re
import dotenv
from datetime import datetime
import datetime
import logging
import asyncio


log = logging.getLogger('bot')

async def run_bot(bot: Bot, cli_flags: Namespace) -> None:
    
    bot.logging.init_logging(
        level=cli_flags.logging_level,
        location=data_manager.core_data_path() / "logs",
        cli_flags=cli_flags,
    )

    log.debug("====Basic Config====")
    log.debug("Data Path: %s", data_manager._base_data_path())
    log.debug("Storage Type: %s", data_manager.storage_type())

    # lib folder has to be in sys.path before trying to load any 3rd-party cog (GH-3061)
    # We might want to change handling of requirements in Downloader at later date
    LIB_PATH = data_manager.cog_data_path(raw_name="Downloader") / "lib"
    LIB_PATH.mkdir(parents=True, exist_ok=True)
    if str(LIB_PATH) not in sys.path:
        sys.path.append(str(LIB_PATH))

        # "It's important to note that the global `working_set` object is initialized from
        # `sys.path` when `pkg_resources` is first imported, but is only updated if you do
        # all future `sys.path` manipulation via `pkg_resources` APIs. If you manually modify
        # `sys.path`, you must invoke the appropriate methods on the `working_set` instance
        # to keep it in sync."
        # Source: https://setuptools.readthedocs.io/en/latest/pkg_resources.html#workingset-objects
        pkg_resources = sys.modules.get("pkg_resources")
        if pkg_resources is not None:
            pkg_resources.working_set.add_entry(str(LIB_PATH))
    sys.meta_path.insert(0, SharedLibImportWarner())

    if cli_flags.token:
        token = cli_flags.token
    else:
        token = os.environ.get("RED_TOKEN", None)
        if not token:
            token = await bot._config.token()

    prefix = cli_flags.prefix or await bot._config.prefix()

    if not (token and prefix):
        if cli_flags.no_prompt is False:
            new_token = await interactive_config(
                bot, token_set=bool(token), prefix_set=bool(prefix)
            )
            if new_token:
                token = new_token
        else:
            log.critical("Token and prefix must be set in order to login.")
            sys.exit(ExitCodes.CONFIGURATION_ERROR)

    if cli_flags.dry_run:
        sys.exit(ExitCodes.SHUTDOWN)
    try:
        # `async with red:` is unnecessary here because we call red.close() in shutdown handler
        await red.start(token)
    except discord.LoginFailure:
        log.critical("This token doesn't seem to be valid.")
        db_token = await red._config.token()
        if db_token and not cli_flags.no_prompt:
            if confirm("\nDo you want to reset the token?"):
                await red._config.token.set("")
                print("Token has been reset.")
                sys.exit(ExitCodes.SHUTDOWN)
        sys.exit(ExitCodes.CONFIGURATION_ERROR)
    except discord.PrivilegedIntentsRequired:
        console = rich.get_console()

        sys.exit(ExitCodes.CONFIGURATION_ERROR)
    except _NoOwnerSet:
        sys.exit(ExitCodes.CONFIGURATION_ERROR)

    return None


def main():
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        loop.set_exception_handler(exc_handler)
        fut = loop.create_task(run_bot(red, cli_flags))
        r_exc_handler = functools.partial(red_exception_handler, red)
        fut.add_done_callback(r_exc_handler)
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(shutdown_handler(red, signal.SIGINT))        

    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        log.info("Please wait, cleaning up a bit more")
        loop.run_until_complete(asyncio.sleep(2))
        asyncio.set_event_loop(None)
        loop.stop()
        loop.close()


if __name__ == "__main__":
    main()
