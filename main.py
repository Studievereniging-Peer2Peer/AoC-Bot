import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from adventofcode import AdventOfCode

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True


bot = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='&', intents=intents)


@bot.event
async def on_ready():
    bot.add_cog(AdventOfCode(bot))
    print("Bot ready\n")


bot.run(TOKEN)
print("Discord token " + TOKEN)
