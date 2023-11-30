import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from adventofcode import AdventOfCode

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if TOKEN is None:
    quit()

intents = discord.Intents.default()
intents.message_content = True


bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='&', intents=intents)


@bot.event
async def on_ready():
    await bot.add_cog(AdventOfCode(bot))
    print("Bot ready\n")


bot.run(TOKEN)
print("Discord token " + TOKEN)
