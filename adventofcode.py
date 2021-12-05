import discord
from discord.ext import commands
from adventofcode_utils.leaderboard import Leaderboard
from adventofcode_utils.utils import Utils
from random import randint
import datetime

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
        embed.set_footer(text="Updated at: {}".format(datetime.datetime.fromtimestamp(self.leaderboard.lastUpdate).strftime('%Y-%m-%d %H:%M:%S')))
        await ctx.send(embed=embed)

    @commands.command(brief="", description="")
    async def user(self, ctx, name="", day=None):
        data = self.leaderboard.get()
        for i, user in data.items():
            if user.name.lower() == name.lower() and day == None:
                embed=discord.Embed(title=user.name, color=0x10941f)
                embed.add_field(name="Position", value=user.position, inline=True)
                embed.add_field(name="Local Score", value=user.score, inline=True)
                embed.add_field(name="Stars", value=user.stars, inline=True)
                embed.set_footer(text='use `&user "{name}" {day}` for detailed day to day information')
                await ctx.send(embed=embed)
                break
            elif user.name.lower() == name.lower() and int(day) < 26:
                embed=discord.Embed(title=user.name, color=0x10941f)
                embed.add_field(name="Day", value=day, inline=True)
                embed.add_field(name="Stars", value=len(user.days[day]), inline=True)
                if len(user.days[day]) > 0:
                    embed.add_field(name="\u200b", value="**Time per star**\n_Part 2 time is the time after completing part 1_", inline=False)
                    if len(user.days[day]) >= 1:
                        embed.add_field(name="Part 1", value=Utils.timeTaken(datetime.datetime(2021, 12, int(day), 6).timestamp(), user.days[day][str(1)]['get_star_ts']), inline=True)
                        if len(user.days[day]) == 2:
                            embed.add_field(name="Part 2", value=Utils.timeTaken(user.days[day][str(1)]['get_star_ts'], user.days[day][str(2)]['get_star_ts']), inline=True)
                await ctx.send(embed=embed)
                break

    @commands.command(brief="", description="")
    async def userCmp(self, ctx, name="", nameCmp="", day=None):
        data = self.leaderboard.get()
        user1 = {}
        user2 = {}
        for i, user in data.items():
            if user.name.lower() == name.lower():
                user1 = user
            if user.name.lower() == nameCmp.lower():
                user2 = user

        embed=discord.Embed(title="**{}** vs **{}** dag **{}**".format(user1.name, user2.name, day), color=0x10941f)

        if user1 is not None and user2 is not None:
            if user1.days[day] == '':
                embed.add_field(name="\u200b", value="**{}** has not done this day".format(user1.name), inline=True)
            elif user2.days[day] == '':
                embed.add_field(name="\u200b", value="**{}** has not done this day".format(user2.name), inline=True)
            else:
                if(int(user1.days[day][str(1)]['get_star_ts']) < int(user2.days[day][str(1)]['get_star_ts'])):
                    embed.add_field(name="Part 1", value="**{}** was {} faster".format(user1.name, Utils.timeTaken(user1.days[day][str(1)]['get_star_ts'], user2.days[day][str(1)]['get_star_ts'])), inline=True)
                else:
                    embed.add_field(name="Part 1", value="**{}** was {} faster".format(user2.name, Utils.timeTaken(user2.days[day][str(1)]['get_star_ts'], user1.days[day][str(1)]['get_star_ts'])), inline=True)
                
                if str(2) not in user1.days[day]:
                    embed.add_field(name="Part2", value="{} has not done part 2 yet".format(user1.name), inline=True)
                elif str(2) not in user2.days[day]:
                    embed.add_field(name="Part2", value="{} has not done part 2 yet".format(user2.name), inline=True)
                else:
                    if(int(user1.days[day][str(2)]['get_star_ts']) < int(user2.days[day][str(2)]['get_star_ts'])):
                        embed.add_field(name="Part 2", value="**{}** was {} faster".format(user1.name, Utils.timeTaken(user1.days[day][str(2)]['get_star_ts'], user2.days[day][str(2)]['get_star_ts'])), inline=True)
                    else:
                        embed.add_field(name="Part 2", value="**{}** was {} faster".format(user2.name, Utils.timeTaken(user2.days[day][str(2)]['get_star_ts'], user1.days[day][str(2)]['get_star_ts'])), inline=True)
        
        await ctx.send(embed=embed)
            