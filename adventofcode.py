import discord
from discord.ext import commands
from leaderboard import Leaderboard
from utils import Utils
from random import randint
import datetime


class AdventOfCode(commands.Cog):
    """Advent of Code"""

    def __init__(self, bot):
        self.leaderboard = Leaderboard()

    @commands.command(brief="Shows the top 20 players",
                      description="Shows the list of the top 20 players, with their local score and obtained stars.")
    async def leaderboard(self, ctx):
        data = self.leaderboard.get()
        names = ""
        score = ""
        stars = ""

        embed = discord.Embed(title="🎄 Peer2Peer Advent of Code leaderboard 🎄",
                              url="https://adventofcode.com/2023/leaderboard/private/view/959961", color=0xC03221)
        for i in range(20):
            if i == 0:
                names += "**🌟 {}: {}**\n".format((i + 1), data[i].name)
                score += "**{}**\n".format(data[i].score)
                stars += "**{}**\n".format(data[i].stars)
            elif i == 1:
                names += "**⭐ {}: {}**\n".format((i + 1), data[i].name)
                score += "**{}**\n".format(data[i].score)
                stars += "**{}**\n".format(data[i].stars)
            elif i == 2:
                names += "**💫 {}: {}**\n".format((i + 1), data[i].name)
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
                names += "{} **{}:** {}\n".format(emote, (i + 1), data[i].name)
                score += "{}\n".format(data[i].score)
                stars += "{}\n".format(data[i].stars)
        embed.add_field(name="Name", value=names, inline=True)
        embed.add_field(name="Score", value=score, inline=True)
        embed.add_field(name="Stars", value=stars, inline=True)
        embed.set_footer(text="Updated at: {}\n🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁".format(
            datetime.datetime.fromtimestamp(self.leaderboard.lastUpdate).strftime('%Y-%m-%d %H:%M:%S')))
        await ctx.send(embed=embed)

    @commands.command(brief="Shows overview of a specific player",
                      description="By adding an optional day argument it will also show the time taken for finished parts.")
    async def user(self, ctx, name="", day=None):
        data = self.leaderboard.get()
        for i, user in data.items():
            if user.name.lower() == name.lower() and day == None:
                embed = discord.Embed(title="{}".format(user.name), color=0x13A10E)
                embed.add_field(name="Position", value=user.position, inline=True)
                embed.add_field(name="Local Score", value=user.score, inline=True)
                if user.globalScore > 0:
                    embed.add_field(name="Global Score", value=user.globalScore, inline=True)
                stars = "\u200b"  # With an additional normal character the star emoji gets smaller on mobile devices, thus fitting better
                # for i in range(round(int(user.stars)/2)):
                for i in range(1, 26):
                    if len(user.days[str(i)]) == 2:
                        stars += "⭐"
                    elif len(user.days[str(i)]) == 1:
                        stars += "<:silver_star:918552091553857536>"
                    else:
                        stars += "<:no_star:918553772739932221>"
                    if i % 5 == 0 and i != 0:
                        stars += "\n";
                embed.add_field(name="Days completed", value=stars, inline=False)
                embed.set_footer(text='🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁')
                await ctx.send(embed=embed)
                break
            elif user.name.lower() == name.lower() and int(day) < 26:
                stars = ""
                if len(user.days[str(day)]) == 2:
                    stars = "⭐"
                elif len(user.days[str(day)]) == 1:
                    stars = "<:silver_star:918552091553857536>"
                embed = discord.Embed(title="{}".format(user.name), description="**Day:** {} {}".format(day, stars),
                                      color=0x13A10E)
                if len(user.days[day]) > 0:
                    if len(user.days[day]) >= 1:
                        embed.add_field(name="Part 1", value=Utils.timeTakenFormatted(
                            datetime.datetime(2023, 12, int(day), 6).timestamp(),
                            user.days[day][str(1)]['get_star_ts']), inline=False)
                        if len(user.days[day]) == 2:
                            embed.add_field(name="Part 2",
                                            value=Utils.timeTakenFormatted(user.days[day][str(1)]['get_star_ts'],
                                                                           user.days[day][str(2)]['get_star_ts']),
                                            inline=False)
                embed.set_footer(text='🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁')
                await ctx.send(embed=embed)
                break

    @commands.command(brief="Compare 2 players their time taken for each day",
                      description="Shows the faster of the 2 players, time is relative to each other.")
    async def userCmp(self, ctx, name="", nameCmp="", day=None):
        data = self.leaderboard.get()
        user1 = {}
        user2 = {}
        for i, user in data.items():
            if user.name.lower() == name.lower():
                user1 = user
            if user.name.lower() == nameCmp.lower():
                user2 = user
            if user1 and user2:
                break

        embed = discord.Embed(title="{} vs {}".format(user1.name, user2.name), description="**Day:** {}".format(day),
                              color=0xFFB900)

        if user1 is not None and user2 is not None:
            if user1.days[day] == '':
                embed.add_field(name="\u200b", value="**{}** has not done this day".format(user1.name), inline=True)
            elif user2.days[day] == '':
                embed.add_field(name="\u200b", value="**{}** has not done this day".format(user2.name), inline=True)
            else:
                if int(user1.days[day][str(1)]['get_star_ts']) < int(user2.days[day][str(1)]['get_star_ts']):
                    embed.add_field(name="Part 1", value="**{}** was {} faster".format(user1.name,
                                                                                       Utils.timeTakenFormatted(
                                                                                           user1.days[day][str(1)][
                                                                                               'get_star_ts'],
                                                                                           user2.days[day][str(1)][
                                                                                               'get_star_ts'])),
                                    inline=False)
                else:
                    embed.add_field(name="Part 1", value="**{}** was {} faster".format(user2.name,
                                                                                       Utils.timeTakenFormatted(
                                                                                           user2.days[day][str(1)][
                                                                                               'get_star_ts'],
                                                                                           user1.days[day][str(1)][
                                                                                               'get_star_ts'])),
                                    inline=False)

                if str(2) not in user1.days[day]:
                    embed.add_field(name="Part2", value="{} has not done part 2 yet".format(user1.name), inline=True)
                elif str(2) not in user2.days[day]:
                    embed.add_field(name="Part2", value="{} has not done part 2 yet".format(user2.name), inline=True)
                else:
                    user1P2 = Utils.timeTaken(user1.days[day][str(1)]['get_star_ts'],
                                              user1.days[day][str(2)]['get_star_ts'])
                    user2P2 = Utils.timeTaken(user2.days[day][str(1)]['get_star_ts'],
                                              user2.days[day][str(2)]['get_star_ts'])
                    if user1P2 < user2P2:
                        # if int(user1.days[day][str(2)]['get_star_ts']) < int(user2.days[day][str(2)]['get_star_ts']):
                        embed.add_field(name="Part 2", value="**{}** was {} faster".format(user1.name,
                                                                                           Utils.timeDeltaFormatted(
                                                                                               user1P2, user2P2)),
                                        inline=False)
                    else:
                        embed.add_field(name="Part 2", value="**{}** was {} faster".format(user2.name,
                                                                                           Utils.timeDeltaFormatted(
                                                                                               user2P2, user1P2)),
                                        inline=False)

        embed.set_footer(text='🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁')
        await ctx.send(embed=embed)

    # @commands.command(brief="Compare 2 players their time taken for each day", description="Shows the faster of the 2 players, time is relative to each other.")
    # async def fastest(self, ctx, day=None):
    #     data = self.leaderboard.get()
    #     part1 = {}
    #     part2 = {}

    #     for i, user in data.items():
    #         if user.days[day] != "":
    #             if user.days[day][str(1)]['get_star_ts'] != None and part1 == None:
    #                 part1 = user
    #             if user.days[day][str(2)]['get_star_ts'] != None and part2 == None:
    #                 part2 = user
    #             else:
    #                 if user.days[day][str(1)]['get_star_ts'] != None:
    #                     if int(user.days[day][str(1)]['get_star_ts']) < int(part1.days[day][str(1)]['get_star_ts']):
    #                         part1 = user
    #                 if user.days[day][str(2)]['get_star_ts'] != None:
    #                     if int(user.days[day][str(2)]['get_star_ts']) < int(part2.days[day][str(2)]['get_star_ts']):
    #                         part2 = user
    #     await ctx.send("{} was fast so was {}".format(part1.name, part2.name))
