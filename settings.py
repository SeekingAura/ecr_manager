import logging
from pathlib import Path
import os
from dotenv import (
    find_dotenv,
    load_dotenv,
    dotenv_values,
)

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(find_dotenv(filename=Path(BASE_DIR, ".env")))


class FilterLogLevelSep(logging.Filter):
    def __init__(self, filter_levels=None):
        super(FilterLogLevelSep, self).__init__()
        self._filter_levels = filter_levels

    #
    def filter(self, record):
        if record.levelname in self._filter_levels:
            return True
        return False


LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
            "style": "%",
        },
        "simple.debug": {
            "format": "%(asctime)s \033[95m%(name)-12s %(levelname)-8s %(message)s\033[0m",
            "style": "%",
        },
        "simple.info": {
            "format": "%(asctime)s \033[96m%(name)-12s %(levelname)-8s %(message)s\033[0m",
            "style": "%",
        },
        "simple.warning": {
            "format": "%(asctime)s \033[93m%(name)-12s %(levelname)-8s %(message)s\033[0m",
            "style": "%",
        },
        "simple.error": {
            "format": "%(asctime)s \033[91m%(name)-12s %(levelname)-8s %(message)s\033[0m",
            "style": "%",
        },
        "simple.critical": {
            "format": "%(asctime)s \33[1m\033[91m%(name)-12s %(levelname)-8s %(message)s\033[0m",
            "style": "%",
        },
    },
    "filters": {
        # Only certain level
        "debug_level_only": {
            "()": FilterLogLevelSep,
            "filter_levels": [
                "DEBUG",
            ],
        },
        "info_level_only": {
            "()": FilterLogLevelSep,
            "filter_levels": [
                "INFO",
            ],
        },
        "warning_level_only": {
            "()": FilterLogLevelSep,
            "filter_levels": [
                "WARNING",
            ],
        },
        "error_level_only": {
            "()": FilterLogLevelSep,
            "filter_levels": [
                "ERROR",
            ],
        },
        "critical_level_only": {
            "()": FilterLogLevelSep,
            "filter_levels": [
                "CRITICAL",
            ],
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "console.debug_only": {
            "class": "logging.StreamHandler",
            "formatter": "simple.debug",
            "filters": ["debug_level_only"],
            "level": "DEBUG",
        },
        "console.info_only": {
            "class": "logging.StreamHandler",
            "formatter": "simple.info",
            "filters": ["info_level_only"],
            "level": "INFO",
        },
        "console.warning_only": {
            "class": "logging.StreamHandler",
            "formatter": "simple.warning",
            "filters": ["warning_level_only"],
            "level": "WARNING",
        },
        "console.error_only": {
            "class": "logging.StreamHandler",
            "formatter": "simple.error",
            "filters": ["error_level_only"],
            "level": "ERROR",
        },
        "console.critical_only": {
            "class": "logging.StreamHandler",
            "formatter": "simple.critical",
            "filters": ["critical_level_only"],
            "level": "CRITICAL",
        },
    },
    "loggers": {
        "": {
            "handlers": [
                "console.debug_only",
                "console.info_only",
                "console.warning_only",
                "console.error_only",
                "console.critical_only",
            ],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
