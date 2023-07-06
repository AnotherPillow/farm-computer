import json

file = open('private/config.json', 'r')
CONFIG = json.load(file)

BOT_TOKEN = CONFIG['token']
BOT_PREFIX = CONFIG['prefix']

IRIDIUM_EMOJI = CONFIG['emojis']['iridium'] # eg. <:iridium:779919999999991040>
GOLD_EMOJI = CONFIG['emojis']['gold']
SILVER_EMOJI = CONFIG['emojis']['silver']