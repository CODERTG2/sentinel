import importlib


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

    if scouting_type == "pit":
        for scout in scouters:
            pass
        await channel.send("Pit Scouting Schedule Set!")
    elif scouting_type == "match":
        for scout in scouters:
            pass
        await channel.send("Match Scouting Schedule Set!")
    else:
        await channel.send("Invalid Type of Scouting!")
