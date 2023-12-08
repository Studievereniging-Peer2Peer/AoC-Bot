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

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='&', intents=intents)

@bot.event
async def on_ready():
    await bot.add_cog(AdventOfCodeCommands(bot))
    print("Bot ready\n")

bot.run(TOKEN)
