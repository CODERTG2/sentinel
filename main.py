import discord
import requests
from bs4 import BeautifulSoup, SoupStrainer
from discord.ext import commands
import re

import tokens
from MyEmbed import MyEmbed

prefix = '$'

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
client.remove_command("help")
client.command_prefix = prefix

comp_code = "2024wimi"
url = "https://www.thebluealliance.com/event/" + comp_code + "#teams"
pit_response = requests.get(url, headers={"X-TBA-Auth-Key": tokens.blueAllianceToken})
pit_soup = BeautifulSoup(pit_response.text, "html.parser", parse_only=SoupStrainer('div', class_='team-name'))
teams_list = pit_soup.find_all('a')

teams = {
    int(re.search(r'/team/(\d+)/', str(team)).group(1)): re.search(r'>(\d+)<br/>(.*)</a>', str(team)).group(2)
    for team in teams_list}


@client.event
async def on_ready():
    print("Bot Connected")  # Alert to notify login of bot


@client.command()
async def scouters(ctx, arg):
    global scouters
    scouters = arg.split(",")
    await ctx.send("Scouters Set!")


@client.command()
async def get_teams(ctx):
    team_items = list(teams.items())
    for i in range(0, len(team_items), 25):
        send_embed = MyEmbed(title=f"Teams at {comp_code}", description="List of teams")
        for team_number, team_name in team_items[i:i + 25]:
            if len(team_name) > 1024:
                team_name = team_name[:1021] + "..."
            send_embed.add_field(name=team_number, value=team_name, inline=False)
        await ctx.send(embed=send_embed)


@client.command
async def assign_pit(ctx):
    for scout in scouters:
        pass
    await ctx.send("Pit Scouting Schedule Set!")


@client.command()
async def assign_match(ctx):
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
