import datetime
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from adventofcode import AdventOfCodeCommands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    print("ERROR: No Discord API token specified.")
    quit()

YEAR = os.getenv('YEAR')

if YEAR is str:
    YEAR = int(YEAR)
elif YEAR is None:
    YEAR = datetime.datetime.now().year

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='&', intents=intents)

@bot.event
async def on_ready():
    await bot.add_cog(AdventOfCodeCommands(YEAR))
    print("Bot ready\n")

bot.run(TOKEN)
