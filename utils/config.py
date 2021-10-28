from os import environ

from dotenv.main import load_dotenv


load_dotenv()


TOKEN = environ.get("TOKEN")
GUILD = environ.get("GUILD")
ADMIN_ROLE = environ.get("ADMIN_ROLE")
BOT_DEV_ROLE = environ.get("BOT_DEV_ROLE")
