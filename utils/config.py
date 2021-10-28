from os import environ

from dotenv.main import load_dotenv


load_dotenv()


TOKEN = environ["TOKEN"]
GUILD = environ["GUILD"]
