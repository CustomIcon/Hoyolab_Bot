import logging
from configparser import ConfigParser
import genshinstats as gs
from bot.bot import bot
import asyncio

# Logging at the start to catch everything
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING,
    handlers=[
        logging.StreamHandler()
    ]
)
LOGS = logging.getLogger(__name__)

name = 'bot'

loop = asyncio.get_event_loop()

# Read from config file
config_file = f"{name}.ini"
config = ConfigParser()
config.read(config_file)

gs.set_cookie(ltuid=config.getint('genshin', 'ltuid'), ltoken=config.get('genshin', 'ltoken')) # login

# Extra details
__version__ = '0.0.1'
__author__ = 'pokurt'

# Global Variables
bot = bot(name)
