import importlib
import random
import re
from itertools import cycle

import teams
from MyEmbed import MyEmbed

scouting_schedule = {}

pairs = []
scouters = []
emojis = [
         "🙂", "😀", "😃", "😄", "😁", "😅", "😆", "🤣", "😂", "🙃", "😉", "😊", "😇", "😎", "🤓", "🧐", "🥳", "😜", "😝",
         "😛", "🤑", "🤠", "🥸", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "😣", "😖", "😫", "😩", "🥺", "😢", "😭",
         "😤", "😠", "😡", "🤬", "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰", "😥", "😓", "🤗", "🤔", "🤭", "🤫", "🤥", "😶",
         "😐", "😑", "😬", "🙄", "😯", "😦", "😧", "😮", "😲", "🥱", "😴", "🤤", "😪", "😵", "🤐", "🥴", "🤢", "🤮", "🤧",
         "😷", "🤒", "🤕", "🤑", "🤠", "🥸", "😏", "😒", "😞", "😔", "😟", "😕", "🙁", "☹️", "😣", "😖", "😫", "😩", "🥺",
         "😢", "😭", "😤", "😠", "😡", "🤬", "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰", "😥", "😓", "🤗", "🤔", "🤭", "🤫",
         "🤥", "😶", "😐", "😑", "😬", "🙄", "😯", "😦", "😧", "😮", "😲", "🥱", "😴", "🤤", "😪", "😵"
]
pit_status = {team_number: "❌" for team_number in teams.teams.keys()}
reaction_embed = []
in_pit = []


async def send_embed(channel, title, description, key_value):
    msg_embed = MyEmbed(title=title, description=description)
    await msg_embed.my_add_field(key_value=key_value, channel=channel, inline=False)


async def on_raw_reaction_add(payload):
    """
    Event that triggers when a reaction is added to a message to update that a team is scouted.

    Parameters:
    payload (discord.RawReactionActionEvent): The payload for the reaction event.

    Returns:
    None
    """

    client = importlib.import_module('main').client

    reaction_embed_id = [embed.id for embed in reaction_embed]

    if payload.message_id in reaction_embed_id:
        user = payload.member
        reaction = payload.emoji

        if str(reaction) in list(emoji_to_team.keys()):
            team_number = emoji_to_team[str(reaction)]
            pit_status[team_number] = "✅"
            await user.send(f"You have completed {team_number}")


async def on_raw_reaction_remove(payload):
    """
    Event that triggers when a reaction is removed to a message to update that a team isn't scouted.

    Parameters:
    payload (discord.RawReactionActionEvent): The payload for the reaction event.

    Returns:
    None
    """

    client = importlib.import_module('main').client

    reaction_embed_id = [embed.id for embed in reaction_embed]

    if payload.message_id in reaction_embed_id:
        user = payload.member
        reaction = payload.emoji

        if str(reaction) in list(emoji_to_team.keys()):
            team_number = emoji_to_team[str(reaction)]
            pit_status[team_number] = "❌"


async def set_scouters(channel, scouters_list: str):
    """
    Sets the scouters for the competition

    Expected format: $set_scouters "(<scouter1ID> <scouter2ID>) (<scouter3ID> <scouter4ID>) ..."

    Parameters:
    channel (discord.Channel): The channel to send messages to.
    scouters_list (str): The list of scouters.

    Returns:
    None
    """
    client = importlib.import_module('main').client

    global pairs
    pairs = re.findall(r'\((.*?)\)', scouters_list)

    global scouters
    scouters = [pair.split() for pair in pairs]
    await channel.send(f"Scouters Set! Current scouters {scouters}")


async def assign(channel, scouting_type: str):
    """
    Assigns teams to scouters based on the scouting type.

    Expected format: $assign <scouting_type>

    Parameters:
    channel (discord.Channel): The channel to send messages to.
    scouting_type (str): The type of scouting. Can be either "pit" or "match".

    Returns:
    None
    """
    client = importlib.import_module('main').client

    if scouting_type == "pit":

        scouters_cycle = cycle(scouters)
        for team in list(teams.teams.keys()):
            scouter = next(scouters_cycle)
            scouting_schedule[team] = scouter

        await channel.send("Pit Scouting Schedule Set! Here is the schedule:")
        # send_embed = MyEmbed(title="Pit Scouting Schedule", description="List of scouters and their assigned teams")
        # await send_embed.my_add_field(key_value=scouting_schedule, channel=channel, inline=False)
        await send_embed(channel,
                         "Pit Scouting Schedule",
                         "List of scouters and their assigned teams",
                         scouting_schedule)

    elif scouting_type == "match":
        for scout in scouters:
            pass
        await channel.send("Match Scouting Schedule Set!")
    else:
        await channel.send("Invalid Type of Scouting!")


emoji_to_team = {emoji: team for emoji, team in zip(emojis, list(teams.teams.keys()))}


async def start(channel, scouting_type: str, num_pairs: int, chosen_pairs: list = None):
    """
    Starts the scouting process.

    Expected format: $start <scouting_type>, <num_pairs>

    Parameters:
    channel (discord.Channel): The channel to send messages to.
    scouting_type (str): The type of scouting. Can be either "pit" or "match".
    num_pairs (int): The number of pairs of scouters to start scouting.

    Returns:
    None
    """
    client = importlib.import_module('main').client

    assigned_teams = []

    if scouting_type == "pit":
        if chosen_pairs is None:
            await channel.send("Pit Scouting Started!")
            chosen_pairs = random.sample(scouters, num_pairs)
            await channel.send(f"Chosen Pairs: {chosen_pairs}")
            msg_embed = MyEmbed(title="Current Scouting Pairs", description="Pairs and their assigned teams")
            for pair in chosen_pairs:
                in_pit.append(pair)
                for scouter in pair:
                    assigned_teams = [team for team, assigned_scouters in scouting_schedule.items() if
                                      scouter in assigned_scouters]
                msg_embed.add_field(name=pair, value=assigned_teams, inline=False)

            assigned_emoji_to_team = {emoji: team for emoji, team in zip(emojis, assigned_teams)}

            emoji_keys = list(assigned_emoji_to_team.keys())
            for i in range(0, len(emoji_keys), 25):
                msg_embed = MyEmbed(title="Current Scouting Pairs", description="Pairs and their assigned teams")
                for emoji in emoji_keys[i:i + 25]:
                    msg_embed.add_field(name=assigned_emoji_to_team[emoji], value=emoji, inline=False)
                reaction_embed.append(await channel.send(embed=msg_embed))
            await channel.send("Good Luck! - https://forms.gle/kLEii5cAaoVD8Y9j9")
        else:
            await channel.send("Pit Scouting Started!")
            await channel.send(f"Chosen Pairs: {chosen_pairs}")
            msg_embed = MyEmbed(title="Current Scouting Pairs", description="Pairs and their assigned teams")
            for pair in chosen_pairs:
                in_pit.append(pair)
                for scouter in pair:
                    assigned_teams = [team for team, assigned_scouters in scouting_schedule.items() if
                                      scouter in assigned_scouters]
                msg_embed.add_field(name=pair, value=assigned_teams, inline=False)

            assigned_emoji_to_team = {emoji: team for emoji, team in zip(emojis, assigned_teams)}

            emoji_keys = list(assigned_emoji_to_team.keys())
            for i in range(0, len(emoji_keys), 25):
                msg_embed = MyEmbed(title="Current Scouting Pairs", description="Pairs and their assigned teams")
                for emoji in emoji_keys[i:i + 25]:
                    msg_embed.add_field(name=assigned_emoji_to_team[emoji], value=emoji, inline=False)
                reaction_embed.append(await channel.send(embed=send_embed))
            await channel.send("Good Luck! - https://forms.gle/kLEii5cAaoVD8Y9j9")
    elif scouting_type == "match":
        await channel.send("Match Scouting Started!")
    else:
        await channel.send("Invalid Type of Scouting!")


async def swap_pairs(channel, old_pair: str, new_pair: str):
    """
    Swaps the scouters in the pairs.

    Expected format: $swap_pairs <pair1> <pair2>

    Parameters:
    channel (discord.Channel): The channel to send messages to.
    pair1 (str): The first pair to swap.
    pair2 (str): The second pair to swap.

    Returns:
    None
    """
    client = importlib.import_module('main').client

    in_pit.remove(old_pair)
    await start(channel, "pit", 1, [new_pair])


async def switch_scouter(channel, scouter1: str, scouter2: str):
    """
    Switches the scouters.

    Expected format: $switch_scouters <scouter1> <scouter2>

    Parameters:
    channel (discord.Channel): The channel to send messages to.
    scouter1 (str): The first scouter to switch.
    scouter2 (str): The second scouter to switch.

    Returns:
    None
    """
    client = importlib.import_module('main').client

    for team, scouter in scouting_schedule.items():
        if scouter == scouter1:
            scouting_schedule[team] = scouter2
        elif scouter == scouter2:
            scouting_schedule[team] = scouter1

    await channel.send(f"Scouters {scouter1} and {scouter2} have been switched!")


async def remove_scouter(channel, old_scouter: str, new_scouter: str):
    """
    Removes a scouter and replaces them with another scouter.

    Expected format: $remove_scouter <removeScouter> <replaceScouter>

    Parameters:
    channel (discord.Channel): The channel to send messages to.
    removeScouter (str): The scouter to remove.
    replaceScouter (str): The scouter to replace the removed scouter with.

    Returns:
    None
    """
    client = importlib.import_module('main').client

    for team, scouter in scouting_schedule.items():
        if scouter == old_scouter:
            scouting_schedule[team] = new_scouter

    await channel.send(f"Scouter {old_scouter} has been removed and replaced with {new_scouter}!")


async def get_status(channel, scouting_type: str):
    """
    Messages the status of the pit scouting.

    Expected format: $get_status <scouting_type>

    Parameters:
    channel (discord.Channel): The channel to send messages to.
    scouting_type (str): The type of scouting. Can be either "pit" or "match".

    Returns:
    None
    """
    client = importlib.import_module('main').client

    if scouting_type == "pit":
        await channel.send("Pit Scouting Status:")
        # send_embed = MyEmbed(title="Pit Scouting Status", description="Status of pit scouting")
        # await send_embed.my_add_field(key_value=pit_status, channel=channel, inline=False)
        await send_embed(channel,
                         "Pit Scouting Status",
                         "Status of pit scouting",
                         pit_status)
        # status_items = list(pit_status.items())
        # for i in range(0, len(status_items), 25):
        #     send_embed = MyEmbed(title="Pit Scouting Status", description="Status of pit scouting")
        #     for team, status in status_items[i:i + 25]:
        #         send_embed.add_field(name=team, value=status, inline=False)
        #     await channel.send(embed=send_embed)
    elif scouting_type == "match":
        pass
    else:
        await channel.send("Invalid Type of Scouting!")


async def scouts_in_pit(channel):
    """
    Messages the scouters in the pit.

    Expected format: $scouts_in_pit

    Parameters:
    channel (discord.Channel): The channel to send messages to.

    Returns:
    None
    """
    client = importlib.import_module('main').client

    await channel.send(f"Scouters in Pit: {in_pit}")


async def get_schedule(channel, scouting_type: str):
    """
    Messages the scouting schedule for the scouting type.

    Expected format: $get_schedule <scouting_type>

    Parameters:
    channel (discord.Channel): The channel to send messages to.
    scouting_type (str): The type of scouting. Can be either "pit" or "match".

    Returns:
    None
    """
    client = importlib.import_module('main').client

    if scouting_type == "pit":
        await channel.send("Pit Scouting Schedule:")
        # send_embed = MyEmbed(title="Pit Scouting Schedule", description="List of scouters and their assigned teams")
        # await send_embed.my_add_field(key_value=scouting_schedule, channel=channel, inline=False)
        await send_embed(channel,
                         "Pit Scouting Schedule",
                         "List of scouters and their assigned teams",
                         scouting_schedule)
    elif scouting_type == "match":
        await channel.send("Match Scouting Schedule:")
    else:
        await channel.send("Invalid Type of Scouting!")


async def get_scouters(channel):
    """
    Messages the list of scouters.

    Expected format: $get_scouters

    Parameters:
    channel (discord.Channel): The channel to send messages to.

    Returns:
    None
    """
    client = importlib.import_module('main').client

    await channel.send("List of Scouters:")
    await channel.send(scouters)
