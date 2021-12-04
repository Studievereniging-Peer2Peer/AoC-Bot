import discord
from discord.ext import commands
from adventofcode_utils.leaderboard import Leaderboard
from adventofcode_utils.utils import Utils
from random import randint
from datetime import datetime

class AdventOfCode(commands.Cog):
    """Advent of Code"""
    def __init__(self, bot):
        self.leaderboard = Leaderboard()

    @commands.command(brief="", description="")
    async def leaderboard(self, ctx):
        data = self.leaderboard.get()
        names = ""
        score = ""
        stars = ""

        embed=discord.Embed(title="🎄 Peer2Peer Advent of Code leaderboard 🎄", url="https://adventofcode.com/2021/leaderboard/private/view/959961", color=0xaf0e0e)
        for i in range(20):
            if i == 0:
                names += "**🌟 {}: {}**\n".format((i+1), data[i].name)
                score += "**{}**\n".format(data[i].score)
                stars += "**{}**\n".format(data[i].stars)
            elif i == 1:
                names += "**⭐ {}: {}**\n".format((i+1), data[i].name)
                score += "**{}**\n".format(data[i].score)
                stars += "**{}**\n".format(data[i].stars)
            elif i == 2:
                names += "**💫 {}: {}**\n".format((i+1), data[i].name)
                score += "**{}**\n".format(data[i].score)
                stars += "**{}**\n".format(data[i].stars)
            else:
                emote = ""
                r = randint(0, 2)  
                if r == 0:
                    emote = "🎄"
                if r == 1:
                    emote = "🎁"
                if r == 2:
                    emote = "🎅"
                names += "{} **{}:** {}\n".format(emote, (i+1), data[i].name)
                score += "{}\n".format(data[i].score)
                stars += "{}\n".format(data[i].stars)
        embed.add_field(name="Name", value=names, inline=True)
        embed.add_field(name="Score", value=score, inline=True)
        embed.add_field(name="Stars", value=stars, inline=True)
        embed.set_footer(text="Updated at: {}".format(datetime.fromtimestamp(self.leaderboard.lastUpdate).strftime('%Y-%m-%d %H:%M:%S')))
        await ctx.send(embed=embed)

    @commands.command(brief="", description="")
    async def user(self, ctx, name="", day=None):
        data = self.leaderboard.get()
        for i, user in data.items():
            if user.name.lower() == name.lower() and day == None:
                embed=discord.Embed(title=user.name, color=0x10941f)
                embed.add_field(name="Position", value=user.position, inline=True)
                embed.add_field(name="Local Score", value=user.score, inline=True)
                embed.add_field(name="Stars", value=user.stars, inline=False)
                embed.set_footer(text='use `&user "{name}" {day}` for detailed day to day information')
                await ctx.send(embed=embed)
                break
            elif user.name.lower() == name.lower() and int(day) < 26:
                embed=discord.Embed(title=user.name, color=0x10941f)
                embed.add_field(name="Day", value=day, inline=True)
                embed.add_field(name="Stars", value=len(user.days[day]), inline=True)
                if len(user.days[day]) > 0:
                    embed.add_field(name="\u200b", value="**Time per star**", inline=False)
                    if len(user.days[day]) >= 1:
                        embed.add_field(name="Star 1", value=Utils.timeTaken(int(day), user.days[day][str(1)]['get_star_ts']), inline=True)
                        if len(user.days[day]) == 2:
                            embed.add_field(name="Star 2", value=Utils.timeTaken(int(day), user.days[day][str(2)]['get_star_ts']), inline=True)
                await ctx.send(embed=embed)
                break