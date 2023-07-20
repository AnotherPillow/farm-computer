import json, discord

file = open('private/config.json', 'r')
CONFIG = json.load(file)

BOT_TOKEN = CONFIG['token']
BOT_PREFIX = CONFIG['prefix']

HELP_MESSAGE_SLASH = CONFIG['help_message_slash'] # specifies if the help message should specify / commands
HELP_PREFIX = '/' if HELP_MESSAGE_SLASH else BOT_PREFIX

IRIDIUM_EMOJI = CONFIG['emojis']['iridium'] # eg. <:iridium:779919999999991040>
GOLD_EMOJI = CONFIG['emojis']['gold']
SILVER_EMOJI = CONFIG['emojis']['silver']
HEALTH_EMOJI = CONFIG['emojis']['health']
ENERGY_EMOJI = CONFIG['emojis']['energy']
COIN_EMOJI = CONFIG['emojis']['coin']
POISON_EMOJI = CONFIG['emojis']['poison']

IRIDIUM_ENERGY_EMOJI = CONFIG['emojis']['iridium_energy']
GOLD_ENERGY_EMOJI = CONFIG['emojis']['gold_energy']
SILVER_ENERGY_EMOJI = CONFIG['emojis']['silver_energy']
IRIDIUM_HEALTH_EMOJI = CONFIG['emojis']['iridium_health']
GOLD_HEALTH_EMOJI = CONFIG['emojis']['gold_health']
SILVER_HEALTH_EMOJI = CONFIG['emojis']['silver_health']
IRIDIUM_POISON_EMOJI = CONFIG['emojis']['iridium_poison']
GOLD_POISON_EMOJI = CONFIG['emojis']['gold_poison']
SILVER_POISON_EMOJI = CONFIG['emojis']['silver_poison']

MAIN_SERVER = CONFIG['main_server_id'] # leave as null to sync all servers
if MAIN_SERVER: MAIN_SERVER = discord.Object(id=MAIN_SERVER)
CMD_CHANS = CONFIG['cmd_chans']

ALLOW_TEXT_COMMANDS = CONFIG['allow_text_commands']
CLEAR_CACHE_HOURS = CONFIG['clear_cache_after_hours']