import logging
import logging.config

from .str_stylizer import str_stylizer
import os


# logger utils
class FilterLogLevelSep(logging.Filter):
    """
    Print only certain level, one level at time
    """

    def __init__(
        self,
        filter_levels: str = "",
    ) -> None:
        super(FilterLogLevelSep, self).__init__()
        self._filter_levels: str = filter_levels

    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelname in self._filter_levels:
            return True
        return False


LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_LEVELS: tuple[str, ...] = (
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL",
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s ",
            "style": "%",
        },
    } | {
        f"simple.{level_i.lower()}": {
            "format": (
                f"%(asctime)s {getattr(str_stylizer, level_i)} %(name)-12s "
                f"%(levelname)-8s %(message)s {str_stylizer.reset}"
            ),
            "style": "%",
        }
        for level_i in LOG_LEVELS
    },
    "filters": {
        f"{level_i.lower()}_level_only": {
            "()": FilterLogLevelSep,
            "filter_levels": [
                level_i,
            ],
        }
        for level_i in LOG_LEVELS
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    } | {
        f"console.{level_i.lower()}_only": {
            "class": "logging.StreamHandler",
            "formatter": f"simple.{level_i.lower()}",
            "filters": [f"{level_i.lower()}_level_only"],
            "level": level_i,
        }
        for level_i in LOG_LEVELS
    },
    "loggers": {
        "": {
            "handlers": [
                f"console.{level_i.lower()}_only" for level_i in LOG_LEVELS
            ],
            "level": LOG_LEVEL,
            "propagate": False,
        },
    },
}

logging.config.dictConfig(LOGGING)
