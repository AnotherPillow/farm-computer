import discord
from discord import app_commands
from discord.ext import commands
import re, requests

from src.config import (
    BOT_TOKEN,
    BOT_PREFIX,
    MAIN_SERVER,
    CMD_CHANS,
    ALLOW_TEXT_COMMANDS,
    WIKITEXT_LINKING,
)

from src.MultiLangLogger.python import Logger
from src.cache import Cache
import src.wiki as _wiki
from src.embed import EmbedBuilder

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

logger = Logger('FarmComputer')
cache = Cache(logger)

link_regex = r'\[\[(.+)\]\]'
bad_link_regex = r'\[\[.+\]\]\(.+\)'

if ALLOW_TEXT_COMMANDS:
    @bot.command()
    async def ping(ctx):
        await ctx.send('pong!')

    @bot.command()
    async def wiki(ctx, *args):
        await ctx.send(embed=_wiki.search(args, _logger=logger))

@app_commands.describe(
    query="What to search the wiki for"
)
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

if WIKITEXT_LINKING:
    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        
        content = str(message.content)
        
        links = re.findall(link_regex, content)
        if links and not re.findall(bad_link_regex, content):
            for link in links:
                r = requests.get(f'https://stardewvalleywiki.com/{link}')

                if r.status_code in [301, 302, 304, 400, 404]:
                    return
                else:
                    await message.reply(f'<https://stardewvalleywiki.com/{link}>', mention_author=False)

@bot.event
async def on_ready():
    await bot.tree.sync(guild=MAIN_SERVER)
    logger.info(f'Bot is ready as {bot.user} ({bot.user.id})')
    print()

bot.run(BOT_TOKEN)