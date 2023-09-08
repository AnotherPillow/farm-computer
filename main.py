import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ext.commands import when_mentioned, when_mentioned_or
from discord.ext.commands.cooldowns import BucketType
import datetime
import traceback
from bs4 import BeautifulSoup
from typing import Optional

from src.config import (
    BOT_TOKEN,
    BOT_PREFIX,
    MAIN_SERVER,
    CMD_CHANS,
    ALLOW_TEXT_COMMANDS,
    CLEAR_CACHE_HOURS
)

from src.logger import Logger
from src.cache import Cache
import src.wiki as _wiki
from src.wiki import _get
from src.embed import EmbedBuilder

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=when_mentioned_or(BOT_PREFIX), intents=intents)

logger = Logger('FarmComputer')
cache = Cache(logger)

emojidict = {
"pong": "\U0001f3d3",
}


#if ALLOW_TEXT_COMMANDS:
    # @bot.command()
    # async def ping(ctx):
    #     await ctx.send('pong!')

    # @bot.command()
    # async def wiki(ctx, *args):
    #     await ctx.send(embed=_wiki.search(args, _logger=logger))


#@wiki.autocomplete("query")


@commands.hybrid_command(name="ping",description="see what the bot's ping is",) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def ping(self, ctx: commands.Context):
    msg: Optional[discord.Message] = None
    a: float = datetime.datetime.now().timestamp()
    if ctx.interaction is None: await ctx.message.add_reaction(str(emojidict.get('pong')))
    else: msg = await ctx.reply("Testing ping...")
    b: float = datetime.datetime.now().timestamp()
    if msg: await msg.edit(content=f"{emojidict.get('pong')} Pong! Latency is `{str(self.bot.latency*1000)}`ms (edit time `{round(b-a)}`).")
    else: await ctx.reply(f"{emojidict.get('pong')} Pong! Latency is `{str(self.bot.latency*1000)}`ms (edit time `{round(b-a)}`).")
    logger.info(f"Latency is {str(self.bot.latency*1000)}ms (edit time {round(b-a)}).")

async def wiki_autocomplete(interaction: discord.Interaction, current: str):
    global allpages

    exact_matches = []
    other_matches = []

    if len(allpages) == 0: return []

    for x in allpages:
        if x.lower().startswith(current.lower()):
            #exact_matches.append(x)
            exact_matches.append(app_commands.Choice(name=x,value=x))
        elif current.lower() in x.lower():
            #other_matches.append(x)
            other_matches.append(app_commands.Choice(name=x,value=x))
        if len(exact_matches) + len(other_matches) >= 25:
            break

    exact_matches.extend(other_matches)

    return list(exact_matches)

WIKI_COMMAND = "</wiki:>"

@bot.hybrid_command(name="wiki", description = "Search the Stardew Valley Wiki for a specific page.")#guild=MAIN_SERVER)
@commands.cooldown(1,5,BucketType.user)
@app_commands.autocomplete(query=wiki_autocomplete)
@app_commands.describe(query="What you want to search the Stardew Valley wiki for.")
async def wiki_slash(ctx: commands.Context, *, query: str):
    start = datetime.datetime.now().timestamp()
    eph = False
    if ctx.guild: eph = ctx.guild.id not in [MAIN_SERVER]
    await ctx.defer(ephemeral=eph)
    if ctx.interaction is None and eph:
        await ctx.reply(f"You can only use the text version of this command in DMs. Use {WIKI_COMMAND} instead.",delete_after=5)
        return
    try: # for text commands, trying to correctly format their query to skip a search request
        proper_query = query
        if proper_query not in allpages:
            for x in allpages:
                if x.lower().strip() == query.lower().strip():
                    proper_query = x
                    break
        emb = await _wiki.search(proper_query.replace(" ","_").replace("'","%27"),cache=cache)
        await ctx.reply(embed=emb)
        end = datetime.datetime.now().timestamp()
        logger.info(f"Looked up {str(emb.title)[:str(emb.title).find('-')-1]} for {ctx.author} in {end-start} seconds.")
    except:
        await ctx.reply(f"No results found for `{query}`. Try searching again.",ephemeral=eph,delete_after=5)
        logger.warn(traceback.format_exc())


prevs = []
running = False

allpages: list[str] = []

async def getallpages(sites: list=[], prev=None) -> list[str]:
    global running, prevs
    r = None
    if prev in prevs: return []
    if not running: 
        running = True
        r = await (await _get('https://stardewvalleywiki.com/Special:AllPages?from=&to=z&namespace=0&hideredirects=1',False)).text()
    else:
        r = await (await _get(prev,False)).text()

    b = BeautifulSoup(r, 'html.parser')


    for found in b.find("ul", {"class": "mw-allpages-chunk"}).find_all("li"):
        sites.append(found.find("a").get("href"))

    for next in b.find_all('a',{"title": "Special:AllPages"}):
        if "Next page" in next.text:    
            r = await getallpages(sites, "https://stardewvalleywiki.com"+next.get("href"))  
            prevs.append("https://stardewvalleywiki.com"+next.get("href"))  
    returnv = []
    for site in sites:
        returnv.append(str(site.replace("%27","'").replace("%20"," ").replace('_'," "))[1:])
    return returnv


@tasks.loop(minutes=30)
async def infloop():
    global allpages, running
    if datetime.datetime.now().minute == 0:
        if not running:
            allpages = await getallpages()
        if CLEAR_CACHE_HOURS <= 0:
            CLEAR_CACHE_HOURS = 5
        else:
            CLEAR_CACHE_HOURS -= 1
        logger.info(f"Clearing cache in {CLEAR_CACHE_HOURS} hours")





@bot.event
async def on_ready():
    await bot.tree.sync(guild=MAIN_SERVER) # dont sync in on_ready
    logger.info(f'Bot is ready as {bot.user} ({bot.user.id})')
    print()

bot.run(BOT_TOKEN)