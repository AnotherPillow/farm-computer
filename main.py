import discord
from discord.ext import commands

from src.config import (
    BOT_TOKEN,
    BOT_PREFIX,
    MAIN_SERVER,
    CMD_CHANS,
    ALLOW_TEXT_COMMANDS,
)

from src.logger import Logger
from src.cache import Cache
import src.wiki as _wiki
from src.embed import EmbedBuilder

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

logger = Logger('FarmComputer')
cache = Cache(logger)


if ALLOW_TEXT_COMMANDS:
    @bot.command()
    async def ping(ctx):
        await ctx.send('pong!')

    @bot.command()
    async def wiki(ctx, *args):
        await ctx.send(embed=_wiki.search(args, _logger=logger))

@bot.tree.command(
    name = "wiki",
    description = "Search the Stardew Valley Wiki for a specific page",
    guild=MAIN_SERVER
)
async def wiki(interaction: discord.Interaction, query: str):
    await interaction.response.defer(
        ephemeral=str(interaction.channel.id) not in CMD_CHANS
    )
    await interaction.followup.send(
        embed=_wiki.search(query, _logger=logger, cache=cache)
    )


@bot.event
async def on_ready():
    await bot.tree.sync(guild=MAIN_SERVER)
    logger.info(f'Bot is ready as {bot.user} ({bot.user.id})')
    print()

bot.run(BOT_TOKEN)