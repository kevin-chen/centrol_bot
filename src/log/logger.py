import logging
import os


def setup_logger():
    # create logger
    logger = logging.getLogger("")
    level = logging.INFO if os.getenv("ENV") == "prod" else logging.DEBUG
    logger.setLevel(level)

    # create console handler and set level to debug
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)
