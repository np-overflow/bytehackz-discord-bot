import logging
from os import environ

from dis_snek.models import to_snowflake
from dotenv.main import load_dotenv


load_dotenv()


TOKEN: str = environ.get("TOKEN")
GUILD: int = to_snowflake(environ.get("GUILD"))
ADMIN_ROLE = to_snowflake(environ.get("ADMIN_ROLE"))
BOT_DEV_ROLE: int = to_snowflake(environ.get("BOT_DEV_ROLE"))
LOGGING_LEVEL: int = int(environ.get("LOGGING_LEVEL", logging.DEBUG))
PARTICIPANT_ROLE = environ.get("PARTICIPANT_ROLE")
MAX_TICKETS: int = int(environ.get("MAX_TICKETS")) #This is probably a bad way to do this :)
GENIUS_ROLE = environ.get("GENIUS_ROLE")
