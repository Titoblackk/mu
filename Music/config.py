##Config

from os import getenv
from dotenv import load_dotenv

load_dotenv()
SESSION_NAME = getenv('SESSION_NAME', 'session')
BOT_TOKEN = getenv('BOT_TOKEN')
OWNER_USERNAME = getenv("OWNER_USERNAME")
API_ID = int(getenv('API_ID', "10892147"))
API_HASH = getenv('API_HASH')
DURATION_LIMIT = int(getenv('DURATION_LIMIT', '30'))
COMMAND_PREFIXES = list(getenv('COMMAND_PREFIXES', '/ . , : ; !').split())
MONGO_DB_URI = getenv("MONGO_DB_URI")
SUDO_USERS = list(map(int, getenv('SUDO_USERS', '').split()))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", '-1001732286742'))
ASS_ID = int(getenv("ASS_ID", '2130437611'))
OWNER_ID = list(map(int, getenv('OWNER_ID', '').split()))
BOT_IMG = getenv("BOT_IMG")
MOT_IMG = getenv("MOT_IMG")
OT_IMG = getenv("OT_IMG")
GROUP = getenv("GROUP", None)
ROUP = getenv("ROUP", None)
CHANNEL = getenv("CHANNEL", None)
HANNEL = getenv("HANNEL", None)
