import re

import requests
from bs4 import BeautifulSoup, SoupStrainer
import importlib

import constants
from MyEmbed import MyEmbed

url = f"https://www.thebluealliance.com/event/{constants.comp_code}#teams"


def fetch_teams():
    """Function to fetch the teams from the Blue Alliance"""
    pit_response = requests.get(url, headers={"X-TBA-Auth-Key": constants.blueAllianceToken})
    pit_soup = BeautifulSoup(pit_response.text, "html.parser", parse_only=SoupStrainer('div', class_='team-name'))
    teams_list = pit_soup.find_all('a')

    return {
        int(re.search(r'/team/(\d+)/', str(team)).group(1)): re.search(r'>(\d+)<br/>(.*)</a>', str(team)).group(2)
        for team in teams_list
    }


teams = fetch_teams()


async def get_teams(channel):
    """
    Command to get the list of teams

    Expected format: $get_teams

    Parameters:
    channel (discord.Channel): The channel to send the message to.

    Returns:
    None
    """
    client = importlib.import_module("main").client
    send_embed = MyEmbed(title=f"Teams at {constants.comp_code}", description="List of teams")
    await send_embed.my_add_field(key_value=teams, channel=channel, inline=False)
    # team_items = list(teams.items())
    # for i in range(0, len(team_items), 25):
    #     send_embed = MyEmbed(title=f"Teams at {constants.comp_code}", description="List of teams")
    #     for team_number, team_name in team_items[i:i + 25]:
    #         if len(team_name) > 1024:
    #             team_name = team_name[:1021] + "..."
    #         send_embed.add_field(name=team_number, value=team_name, inline=False)
    #     await channel.send(embed=send_embed)


async def add_team(channel, team_number: int, team_name: str):
    """
    Command to add a team to the list of teams

    Expected format: $add_team <team_number>, <team_name>

    Parameters:
    channel (discord.Channel): The channel to send the message to.
    team_number (int): The number of the team to add.
    team_name (str): The name of the team to add.

    Returns:
    None
    """
    client = importlib.import_module("main").client

    teams[team_number] = team_name
    await channel.send("Team Added! Here is the new list of teams:")
    await get_teams(channel)


async def remove_team(channel, team_number: int):
    """
    Command to remove a team from the list of teams

    Expected format: $remove_team <team_number>

    Parameters:
    channel (discord.Channel): The channel to send the message to.
    team_number (int): The number of the team to remove.

    Returns:
    None
    """
    client = importlib.import_module("main").client

    del teams[team_number]
    await channel.send("Team Removed! Here is the new list of teams:")
    await get_teams(channel)
