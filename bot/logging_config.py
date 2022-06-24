ERROR_LOG_FILENAME = "bot.log"

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s:%(name)s:%(process)d[LINE]:%(lineno)d " "%(levelname)s %(message)s",
            "datefmt": "[DATE]%d.%m.%Y[TIME]%H:%M:%S",
        },
        "simple": {
            "format": "%(asctime)s:%(levelname)s[BOT]:%(message)s",
            "datefmt": "[DATE]%d.%m.%Y[TIME]%H:%M:%S",
        },
    },
    "handlers": {
        "logfile": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "ERROR",
            "filename": ERROR_LOG_FILENAME,
            "formatter": "default",
            "backupCount": 2,
        },
        "verbose_output": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "tryceratops": {
            "level": "INFO",
            "handlers": [
                "verbose_output",
            ],
        },
    },
    "root": {"level": "INFO", "handlers": ["logfile", "verbose_output"]},
}