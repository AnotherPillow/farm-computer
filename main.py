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
async def embed(ctx):
    await ctx.send(embed=EmbedBuiler(
        title='Test',
        description='This is a test embed',
        fields=[
            {
                'name': 'Field 1',
                'value': 'This is the first field',
                'inline': True
            },
            {
                'name': 'Field 2',
                'value': 'This is the second field',
                'inline': True
            },
        ],
        color=discord.Color.green(),
        footer='This is a footer',
        thumbnail='https://lh3.googleusercontent.com/a-/AOh14GjFj_pNcy1DaeyoTVg1VXs4CikM6RcMb3CX-dSJCQ=k-s256',
        image='https://lh4.googleusercontent.com/-IaAtZYC9o5o/AAAAAAAAAAI/AAAAAAAAAYM/r6SDDsfCoOc/photo.jpg?sz=256'
    ).build())
        

@bot.command()
async def wiki(ctx, *args):
    await ctx.send(embed=_wiki.search(args, _logger=logger))


@bot.event
async def on_ready():
    logger.info(f'Bot is ready as {bot.user} ({bot.user.id})')
    print()

bot.run(BOT_TOKEN)