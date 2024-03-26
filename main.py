import discord
from discord.ext import commands

import constants
from scouters import set_scouters, assign, get_schedule, get_scouters, start, on_raw_reaction_add, \
    on_raw_reaction_remove, get_status, switch_scouter, remove_scouter, swap_pairs
from teams import fetch_teams, get_teams, add_team, remove_team

prefix = '$'

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
# client.remove_command("help")
client.command_prefix = prefix

teams = fetch_teams()


@client.event
async def on_ready():
    """Event that triggers when the bot is ready to be used."""
    print("Bot Connected")  # Alert to notify login of bot


@client.command()
async def set_comp(ctx, competition_code: str):
    """
    Sets the competition code for the bot

    Expected format: $set_comp <competition_code>

    Parameters:
    ctx (discord.Context): The context of the command.
    competition_code (str): The competition code to set.

    Returns:
    None
    """
    constants.comp_code = competition_code
    await ctx.send(f"Competition Code Set to {competition_code}")

client.add_listener(on_raw_reaction_add, 'on_raw_reaction_add')
client.add_listener(on_raw_reaction_remove, 'on_raw_reaction_remove')


client.add_command(commands.Command(get_teams))
client.add_command(commands.Command(add_team))
client.add_command(commands.Command(remove_team))

client.add_command(commands.Command(set_scouters))
client.add_command(commands.Command(assign))
client.add_command(commands.Command(start))
client.add_command(commands.Command(swap_pairs))
client.add_command(commands.Command(switch_scouter))
client.add_command(commands.Command(remove_scouter))
client.add_command(commands.Command(get_status))
client.add_command(commands.Command(get_schedule))
client.add_command(commands.Command(get_scouters))


if __name__ == "__main__":
    client.run(constants.botToken)
