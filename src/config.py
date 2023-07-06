import json

file = open('private/config.json', 'r')
CONFIG = json.load(file)

BOT_TOKEN = CONFIG['token']
BOT_PREFIX = CONFIG['prefix']