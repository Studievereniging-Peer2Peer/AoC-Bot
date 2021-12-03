import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from adventofcode import AdventOfCode

load_dotenv()   
TOKEN = os.getenv('DISCORD_TOKEN')

bot = discord.Client()
bot = commands.Bot(command_prefix='&')

@bot.event
async def on_ready():
    bot.add_cog(AdventOfCode(bot))
    print("Bot ready\n")

bot.run(TOKEN)