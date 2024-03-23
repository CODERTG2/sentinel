import discord
import requests
from bs4 import BeautifulSoup, SoupStrainer
from discord.ext import commands

import tokens

prefix = '$'

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
client.remove_command("help")
client.command_prefix = prefix


@client.event
async def on_ready():
    print("Bot Connected")  # Alert to notify login of bot


@client.command()
async def get_teams(ctx):
        URL = "https://www.thebluealliance.com/event/" + "2024wimi" + "#teams"
        pitResponse = requests.get(URL, headers={"X-TBA-Auth-Key": tokens.blueAllianceToken})
        pitSoup = BeautifulSoup(pitResponse.text, "html.parser", parse_only=SoupStrainer('div', class_='team-name'))
        teamsList = pitSoup.find_all('a')

        teams = {}

        for team in teamsList:
            # hardcoded for the first term. something like this is needed.
            team = str(team)
            teamNumber = team.replace('<a href="/team/', '')
            teamNumberList = []

            for char in list(teamNumber):
                teamNumberList.append(char)

                if char == '/':
                    break

            for number in teamNumberList:
                teamNumber += number
            teamNumber = int(teamNumber)

            print(teamNumber)

            teamName = team.replace(f'<a href="/team/{int(teamNumber)}/2024">{int(teamNumber)}<br/>', '')
            teamName = team.replace('</a>', '')
            teams[teamNumber] = teamName

        print(teams)
        await ctx.send("pitSoup.prettify()")


@client.command
async def assign_pit(ctx, arg):
    scouters = arg.split(",")
    for scout in scouters:
        pass
    await ctx.send("Pit Scouting Schedule Set!")


@client.command()
async def assign_match(ctx, arg):
    scouters = arg.split(",")
    for scout in scouters:
        pass
    await ctx.send("Match Scouting Schedule Set!")


@client.command()
async def current(ctx, arg):
    if arg == "pit":
        await ctx.send("pit")
    if arg == "match":
        await ctx.send("match")


client.run(tokens.botToken)
