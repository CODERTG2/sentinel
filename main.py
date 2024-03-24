import discord
from discord.ext import commands

import constants
from scouters import set_scouters, assign_pit, assign_match
from teams import fetch_teams, get_teams

prefix = '$'

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
client.remove_command("help")
client.command_prefix = prefix

teams = fetch_teams()


@client.event
async def on_ready():
    """Event that triggers when the bot is ready to be used."""
    print("Bot Connected")  # Alert to notify login of bot

client.add_command(commands.Command(set_scouters))
client.add_command(commands.Command(get_teams))
client.add_command(commands.Command(assign_pit))
client.add_command(commands.Command(assign_match))


@client.command()
async def current(ctx, arg):
    if arg == "pit":
        await ctx.send("pit")
    if arg == "match":
        await ctx.send("match")

if __name__ == "__main__":
    client.run(constants.botToken)
