import discord
import requests
from bs4 import BeautifulSoup, SoupStrainer
from discord.ext import commands
import re

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

        teams = {
            int(re.search(r'/team/(\d+)/', str(team)).group(1)): re.search(r'>(\d+)<br/>(.*)</a>', str(team)).group(2)
            for team in teamsList}

        await ctx.send(teams)


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
