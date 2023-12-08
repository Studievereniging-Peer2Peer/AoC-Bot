import discord
from discord.ext import commands
from aocapi import AoCAPI
import utils
from random import randint
import datetime
import random


class AdventOfCodeCommands(commands.Cog):
    """Advent of Code"""

    def __init__(self, bot):
        self.aoc_api = AoCAPI()

    @commands.command(brief="Shows the top 20 players",
                      description="Shows the list of the top 20 players, with their local score and obtained stars.")
    async def leaderboard(self, ctx):
        leaderboard_users = self.aoc_api.get_leaderboard()
        names = ""
        score = ""
        stars = ""

        embed = discord.Embed(title="🎄 Peer2Peer Advent of Code leaderboard 🎄",
                              url="https://adventofcode.com/2023/leaderboard/private/view/959961", color=0xC03221)
        for i in range(20):
            user = leaderboard_users[i]
            if i == 0:
                names += f"**🌟 {user.leaderboard_position}: {user.name}**\n"
                score += f"**{user.localScore}**\n"
                stars += f"**{user.stars_amount}**\n"
            elif i == 1:
                names += f"**⭐ {user.leaderboard_position}: {user.name}**\n"
                score += f"**{user.localScore}**\n"
                stars += f"**{user.stars_amount}**\n"
            elif i == 2:
                names += f"**💫 {user.leaderboard_position}: {user.name}**\n"
                score += f"**{user.localScore}**\n"
                stars += f"**{user.stars_amount}**\n"
            else:
                emote = random.choice(["🎄", "🎁", "🎅"])
                names += f"{emote} **{user.leaderboard_position}:** {user.name}\n"
                score += f"{user.localScore}\n"
                stars += f"{user.stars_amount}\n"
        embed.add_field(name="Name", value=names, inline=True)
        embed.add_field(name="Score", value=score, inline=True)
        embed.add_field(name="Stars", value=stars, inline=True)
        embed.set_footer(text="Updated at: {}\n🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁".format(
            datetime.datetime.fromtimestamp(self.aoc_api.lastUpdate).strftime('%Y-%m-%d %H:%M:%S')))
        await ctx.send(embed=embed)

    @commands.command(brief="Shows overview of a specific player",
                      description="By adding an optional day argument it will also show the time taken for finished parts.")
    async def user(self, ctx, name: str = "", day: int | None = None):
        leaderboard_users = self.aoc_api.get_leaderboard()

        user = utils.getUserFromLeaderboard(leaderboard_users, name)

        if not user:
            embed = discord.Embed(
                title=f"User {name} was not found."
            )
            ctx.send(embed=embed)
            return

        if day == None:
            embed = discord.Embed(
                title="{}".format(user.name), color=0x13A10E)
            embed.add_field(name="Position",
                            value=user.leaderboard_position, inline=True)
            embed.add_field(name="Local Score",
                            value=user.localScore, inline=True)
            if user.globalScore > 0:
                embed.add_field(name="Global Score",
                                value=user.globalScore, inline=True)

            stars = "\u200b"  # With an additional normal character the star emoji gets smaller on mobile devices, thus fitting better
            for i in range(1, 26):
                if user.days[i].get_star_2_ts != None:
                    stars += "⭐"
                elif user.days[i].get_star_1_ts != None:
                    stars += "<:silver_star:918552091553857536>"
                else:
                    stars += "<:no_star:918553772739932221>"
                if i % 5 == 0 and i != 0:
                    stars += "\n"
            embed.add_field(name="Days completed",
                            value=stars, inline=False)
            embed.set_footer(text="Updated at: {}\n🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁".format(
                datetime.datetime.fromtimestamp(self.aoc_api.lastUpdate).strftime('%Y-%m-%d %H:%M:%S')))
            await ctx.send(embed=embed)
        elif day > 0 and day <= 26:
            stars = ""
            if user.days[day].get_star_2_ts != None:
                stars = "⭐"
            elif user.days[day].get_star_1_ts != None:
                stars = "<:silver_star:918552091553857536>"
            else:
                stars = "<:no_star:918553772739932221>"
            embed = discord.Embed(title=user.name, description=f"**Day:** {day} {stars}",
                                  color=0x13A10E)

            if user.days[day].get_star_1_ts != None:
                val = utils.timeTakenFormatted(
                    datetime.datetime(
                        2023, 12, int(day), 6).timestamp(),
                    user.days[day].get_star_1_ts)
                embed.add_field(name="Part 1", value=val, inline=False)

            if user.days[day].get_star_2_ts != None:
                val = utils.timeTakenFormatted(user.days[day].get_star_1_ts,
                                               user.days[day].get_star_2_ts)
                embed.add_field(name="Part 2", value=val, inline=False)

            embed.set_footer(text="Updated at: {}\n🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁".format(
                datetime.datetime.fromtimestamp(self.aoc_api.lastUpdate).strftime('%Y-%m-%d %H:%M:%S')))
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f"The command could not be completed."
            )
            ctx.send(embed=embed)
            return

    @commands.command(brief="Compare time taken for two players on a given day",
                      description="Shows the faster of the 2 players, time is relative to each other.")
    async def userCmp(self, ctx, name1="", name2="", day: int | None = None):
        leaderboard_users = self.aoc_api.get_leaderboard()

        if not day:
            embed = discord.Embed(
                title=f"You must specify a day."
            )
            ctx.send(embed=embed)
            return

        user1 = utils.getUserFromLeaderboard(leaderboard_users, name1)
        user2 = utils.getUserFromLeaderboard(leaderboard_users, name2)

        if not user1 or not user2:
            embed = discord.Embed(
                title=f"The users specified could not be found."
            )
            ctx.send(embed=embed)
            return

        embed = discord.Embed(title=f"{user1.name} vs {user2.name}", description=f"**Day:** {day}",
                              color=0xFFB900)

        user1_star1_ts = user1.days[day].get_star_1_ts
        user2_star1_ts = user2.days[day].get_star_1_ts

        if user1_star1_ts == None or user2_star1_ts == None:
            embed.add_field(name="Part 1",
                            value="Not all users have completed this part.",
                            inline=False)
        else:
            if user1_star1_ts < user2_star1_ts:
                embed.add_field(name="Part 1",
                                value=f"**{user1.name}** was {utils.timeTakenFormatted(user1_star1_ts,
                                                                                        user2_star1_ts)} faster",
                                inline=False)
            else:
                embed.add_field(name="Part 1",
                                value=f"**{user2.name}** was {utils.timeTakenFormatted(user2_star1_ts,
                                                                                        user1_star1_ts)} faster",
                                inline=False)

        user1_star2_ts = user1.days[day].get_star_2_ts
        user2_star2_ts = user2.days[day].get_star_2_ts

        if user1_star2_ts == None or user2_star2_ts == None:
            embed.add_field(name="Part 2",
                            value="Not all users have completed this part.",
                            inline=False)
        else:
            if user1_star2_ts < user2_star2_ts:
                embed.add_field(name="Part 2",
                                value=f"**{user1.name}** was {utils.timeTakenFormatted(user1_star2_ts,
                                                                                    user2_star2_ts)} faster",
                                inline=False)
            else:
                embed.add_field(name="Part 2",
                                value=f"**{user2.name}** was {utils.timeTakenFormatted(user2_star2_ts,
                                                                                    user1_star2_ts)} faster",
                                inline=False)

        embed.set_footer(text="Updated at: {}\n🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁🎄🎁".format(
                datetime.datetime.fromtimestamp(self.aoc_api.lastUpdate).strftime('%Y-%m-%d %H:%M:%S')))
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
