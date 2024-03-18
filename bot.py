import discord
from discord.ext import commands

token = "MTIxODMxMTQ2NzExMjA3NTM3NQ.G1PQG_.nQmH72Gz26v0J_9mzj3OOTz8AWgxP7AHs8TxAo"

prefix = '$'

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
client.remove_command("help")
client.command_prefix = prefix


@client.event
async def on_ready():
    print("Bot Connected")  # Alert to notify login of bot


@client.command()
async def current(ctx, arg):
    # await ctx.send("it works")
    if arg == "pit":
        await ctx.send("pit")
    if arg == "match":
        await ctx.send("match")


client.run(token)