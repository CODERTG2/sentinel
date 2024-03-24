import re

import requests
from bs4 import BeautifulSoup, SoupStrainer
import importlib

import constants
from MyEmbed import MyEmbed


url = f"https://www.thebluealliance.com/event/{constants.comp_code}#teams"


def fetch_teams():
    pit_response = requests.get(url, headers={"X-TBA-Auth-Key": constants.blueAllianceToken})
    pit_soup = BeautifulSoup(pit_response.text, "html.parser", parse_only=SoupStrainer('div', class_='team-name'))
    teams_list = pit_soup.find_all('a')
    return {
        int(re.search(r'/team/(\d+)/', str(team)).group(1)): re.search(r'>(\d+)<br/>(.*)</a>', str(team)).group(2)
        for team in teams_list
    }


async def get_teams(ctx):
    """Command to get the list of teams"""
    client = importlib.import_module("main").client

    team_items = list(fetch_teams().items())
    for i in range(0, len(team_items), 25):
        send_embed = MyEmbed(title=f"Teams at {constants.comp_code}", description="List of teams")
        for team_number, team_name in team_items[i:i + 25]:
            if len(team_name) > 1024:
                team_name = team_name[:1021] + "..."
            send_embed.add_field(name=team_number, value=team_name, inline=False)
        await ctx.send(embed=send_embed)
