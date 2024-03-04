import logging.config

# noinspection SpellCheckingInspection
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "[{asctime}.{msecs:03.0f}] [{levelname}] [{threadName}] [{name}:{lineno:.0f}] {message}",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "style": "{",
        }
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "console"}},
    "loggers": {
        "urllib3": {"level": "INFO"},
    },
    "root": {"handlers": ["console"], "level": "NOTSET"},
}


def init_logger(logger_name: str) -> logging.Logger:
    """Configure logging and return a logger with the specified name.

    Args:
        logger_name: specified name (channel name) for logger.

    Returns:
        Fully configured logger.
    """
    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger(logger_name)

    logger.debug(f"Logging configuration done")

    return logger
