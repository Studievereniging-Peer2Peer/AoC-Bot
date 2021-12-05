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

        embed=discord.Embed(title="🎄 Peer2Peer Advent of Code leaderboard 🎄", url="https://adventofcode.com/2021/leaderboard/private/view/959961", color=0xC03221)
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
        embed.set_footer(text="Updated at: {}\n🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄".format(datetime.datetime.fromtimestamp(self.leaderboard.lastUpdate).strftime('%Y-%m-%d %H:%M:%S')))
        await ctx.send(embed=embed)

    @commands.command(brief="", description="")
    async def user(self, ctx, name="", day=None):
        data = self.leaderboard.get()
        for i, user in data.items():
            if user.name.lower() == name.lower() and day == None:
                embed=discord.Embed(title="{}".format(user.name), color=0x13A10E)
                embed.add_field(name="Position", value=user.position, inline=True)
                embed.add_field(name="Local Score", value=user.score, inline=True)
                stars = ""
                for i in range(round(int(user.stars)/2)):
                    stars += "⭐"
                embed.add_field(name="Days completed", value=stars, inline=False)
                embed.set_footer(text='use `&user "{name}" {day}` for detailed day to day information\n🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁')
                await ctx.send(embed=embed)
                break
            elif user.name.lower() == name.lower() and int(day) < 26:
                stars = ""
                for i in range(len(user.days[day])):
                    stars += "⭐"
                embed=discord.Embed(title="{}".format(user.name), description="**Day:** {} **Stars:** {}".format(day, stars), color=0x13A10E)
                if len(user.days[day]) > 0:
                    if len(user.days[day]) >= 1:
                        embed.add_field(name="Part 1", value=Utils.timeTaken(datetime.datetime(2021, 12, int(day), 6).timestamp(), user.days[day][str(1)]['get_star_ts']), inline=False)
                        if len(user.days[day]) == 2:
                            embed.add_field(name="Part 2", value=Utils.timeTaken(user.days[day][str(1)]['get_star_ts'], user.days[day][str(2)]['get_star_ts']), inline=False)
                embed.set_footer(text='🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄')
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

        embed=discord.Embed(title="{} vs {}".format(user1.name, user2.name), description="**Day:** {}".format(day), color=0xFFB900)

        if user1 is not None and user2 is not None:
            if user1.days[day] == '':
                embed.add_field(name="\u200b", value="**{}** has not done this day".format(user1.name), inline=True)
            elif user2.days[day] == '':
                embed.add_field(name="\u200b", value="**{}** has not done this day".format(user2.name), inline=True)
            else:
                if(int(user1.days[day][str(1)]['get_star_ts']) < int(user2.days[day][str(1)]['get_star_ts'])):
                    embed.add_field(name="Part 1", value="**{}** was {} faster".format(user1.name, Utils.timeTaken(user1.days[day][str(1)]['get_star_ts'], user2.days[day][str(1)]['get_star_ts'])), inline=False)
                else:
                    embed.add_field(name="Part 1", value="**{}** was {} faster".format(user2.name, Utils.timeTaken(user2.days[day][str(1)]['get_star_ts'], user1.days[day][str(1)]['get_star_ts'])), inline=False)
                
                if str(2) not in user1.days[day]:
                    embed.add_field(name="Part2", value="{} has not done part 2 yet".format(user1.name), inline=True)
                elif str(2) not in user2.days[day]:
                    embed.add_field(name="Part2", value="{} has not done part 2 yet".format(user2.name), inline=True)
                else:
                    if(int(user1.days[day][str(2)]['get_star_ts']) < int(user2.days[day][str(2)]['get_star_ts'])):
                        embed.add_field(name="Part 2", value="**{}** was {} faster".format(user1.name, Utils.timeTaken(user1.days[day][str(2)]['get_star_ts'], user2.days[day][str(2)]['get_star_ts'])), inline=False)
                    else:
                        embed.add_field(name="Part 2", value="**{}** was {} faster".format(user2.name, Utils.timeTaken(user2.days[day][str(2)]['get_star_ts'], user1.days[day][str(2)]['get_star_ts'])), inline=False)
        
        embed.set_footer(text='🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄')
        await ctx.send(embed=embed)
            