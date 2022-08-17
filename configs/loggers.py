import logging


def get_battery_level_logger() -> logging.Logger:
    logger = logging.getLogger("battery_level_logger")
    logger_handler = logging.FileHandler('file.log')
    # logger_handler.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO)
    logger_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(message)s')
    logger_handler.setFormatter(logger_formatter)
    logger.addHandler(logger_handler)

    return logger
