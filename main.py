import discord
from discord.ext import commands

from src.config import (
    BOT_TOKEN,
    BOT_PREFIX
)

from src.logger import Logger
import src.wiki as _wiki
from src.embed import EmbedBuiler

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

logger = Logger('FarmComputer')

@bot.command()
async def ping(ctx):
    await ctx.send('pong!')

@bot.command()
async def wiki(ctx, *args):
    await ctx.send(embed=_wiki.search(args, _logger=logger))

@bot.event
async def on_ready():
    logger.info(f'Bot is ready as {bot.user} ({bot.user.id})')
    print()

bot.run(BOT_TOKEN)