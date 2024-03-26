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
emoji_to_team = {}
pit_status = {team_number: "❌" for team_number in teams.teams.keys()}
reaction_embed = []


async def set_scouters(channel, scouters_list: str):
    """
    Sets the scouters for the competition

    Expected format: $set_scouters "(<scouter1ID> <scouter2ID>) (<scouter3ID> ..."

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

        schedule_items = list(scouting_schedule.items())
        for i in range(0, len(schedule_items), 25):
            send_embed = MyEmbed(title="Pit Scouting Schedule", description="List of scouters and their assigned teams")
            for scouter, team in schedule_items[i:i + 25]:
                send_embed.add_field(name=scouter, value=team, inline=False)
            await channel.send(embed=send_embed)

    elif scouting_type == "match":
        for scout in scouters:
            pass
        await channel.send("Match Scouting Schedule Set!")
    else:
        await channel.send("Invalid Type of Scouting!")


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
        schedule_items = list(scouting_schedule.items())
        for i in range(0, len(schedule_items), 25):
            send_embed = MyEmbed(title="Pit Scouting Schedule", description="List of scouters and their assigned teams")
            for scouter, team in schedule_items[i:i + 25]:
                send_embed.add_field(name=scouter, value=team, inline=False)
            await channel.send(embed=send_embed)
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


async def start(channel, scouting_type: str, num_pairs: int):
    """
    Starts the scouting process.

    Expected format: $start <scouting_type>

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
        await channel.send("Pit Scouting Started!")
        chosen_pairs = random.sample(scouters, num_pairs)
        await channel.send(f"Chosen Pairs: {chosen_pairs}")
        send_embed = MyEmbed(title="Current Scouting Pairs", description=f"Pairs and their assigned teams")
        for pair in chosen_pairs:
            for scouter in pair:
                assigned_teams = [team for team, assigned_scouters in scouting_schedule.items() if
                                  scouter in assigned_scouters]
            send_embed.add_field(name=pair, value=assigned_teams, inline=False)
        global emoji_to_team
        emoji_to_team = {emoji: team for emoji, team in zip(emojis, assigned_teams)}
        emoji_keys = list(emoji_to_team.keys())
        global reaction_embed
        for i in range(0, len(emoji_keys), 25):
            send_embed = MyEmbed(title="Current Scouting Pairs", description=f"Pairs and their assigned teams")
            for emoji in emoji_keys[i:i + 25]:
                send_embed.add_field(name=emoji_to_team[emoji], value=emoji, inline=False)
            reaction_embed.append(await channel.send(embed=send_embed))
        await channel.send("Good Luck! - https://forms.gle/kLEii5cAaoVD8Y9j9")
    elif scouting_type == "match":
        await channel.send("Match Scouting Started!")
    else:
        await channel.send("Invalid Type of Scouting!")


async def on_raw_reaction_add(payload):
    """
    Event that triggers when a reaction is added to a message.

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

        print(f"Reaction added by user {payload.user_id} with emoji {payload.emoji}")

        print(emoji_to_team)
        if str(reaction) in list(emoji_to_team.keys()):
            print(f"In if statement - Reaction added by user {payload.user_id} with emoji {payload.emoji}")
            team_number = emoji_to_team[str(reaction)]
            pit_status[team_number] = "✅"
            await user.send(f"You have completed {team_number}")
