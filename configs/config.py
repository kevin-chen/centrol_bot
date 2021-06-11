import os
import logging
from enum import Enum

log = logging.getLogger(__name__)


class ENV(Enum):
    DEV = "DEV"
    PROD = "PROD"


class CentrolConfig:

    log.info("Setting up ..")
    env = ENV.PROD if os.getenv("ENV") == "prod" else ENV.DEV

    def __init__(self):

        if self.env == ENV.PROD:
            """
            Production configurations
            """
            self.DEBUG = False
            self.URL = "127.0.0.1"
            self.PORT = 8080

        else:
            """
            Development configurations
            """
            self.DEBUG = True
            self.SQLALCHEMY_ECHO = True
            self.ASSETS_DEBUG = True
            self.URL = "127.0.0.1"
            self.PORT = 8080

            log.warn(
                "THIS APP IS IN DEBUG MODE. YOU SHOULD NOT SEE THIS IN PRODUCTION."
            )
