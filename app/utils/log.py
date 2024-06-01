import logging
from logging import handlers
from pathlib import Path
import coloredlogs
import os
import sys
from pydis_core.utils import logging as core_logging
import constants

get_logger = logging.getLogger('bot')

def setup() ->None:
    root_log = get_logger
    
    if constants.FILE_LOGS:
        log_file = Path("logs", "bot.log")
        log_file.parent.mkdir(exist_ok=True)
        file_handler = handlers.RotatingFileHandler(log_file, maxBytes=5242880, backupCount=7, encoding="utf8")
        root_log.addHandler(file_handler)

    if "COLOREDLOGS_LEVEL_STYLES" not in os.environ:
        coloredlogs.DEFAULT_LEVEL_STYLES = {
            **coloredlogs.DEFAULT_LEVEL_STYLES,
            "trace": {"color": 246},
            "critical": {"background": "red"},
            "debug": coloredlogs.DEFAULT_LEVEL_STYLES["info"]
        }

    if "COLOREDLOGS_LOG_FORMAT" not in os.environ:
        coloredlogs.DEFAULT_LOG_FORMAT = core_logging.log_format._fmt

    coloredlogs.install(level=core_logging.TRACE_LEVEL, logger=root_log, stream=sys.stdout)
    root_log.setLevel(logging.DEBUG if constants.DEBUG_MODE else logging.INFO)