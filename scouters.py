import importlib
from itertools import cycle

import teams
from MyEmbed import MyEmbed


async def set_scouters(channel, scouters_list: str):
    """Sets the scouters for the competition"""
    client = importlib.import_module('main').client

    global scouters
    scouters = scouters_list.split(",")
    await channel.send("Scouters Set!")


async def assign(channel, scouting_type: str):
    """
    Assigns scouting to scouters based on the scouting type.

    Parameters:
    channel (discord.Channel): The channel to send messages to.
    scouting_type (str): The type of scouting. Can be either "pit" or "match".

    Returns:
    None
    """
    client = importlib.import_module('main').client

    scouting_schedule = {}
    if scouting_type == "pit":

        scouters_cycle = cycle(scouters)
        for team in list(teams.teams.keys()):
            scouter = next(scouters_cycle)
            scouting_schedule[team] = scouter
        await channel.send("Pit Scouting Schedule Set! Here is the schedule:")

        schedule_items = list(scouting_schedule.items())
        for i in range(0, len(schedule_items), 25):
            send_embed = MyEmbed(title="Pit Scouting Schedule",
                                description="List of scouters and their assigned teams")
            for scouter, team in schedule_items[i:i + 25]:
                send_embed.add_field(name=scouter, value=team, inline=False)
            await channel.send(embed=send_embed)

    elif scouting_type == "match":
        for scout in scouters:
            pass
        await channel.send("Match Scouting Schedule Set!")
    else:
        await channel.send("Invalid Type of Scouting!")
