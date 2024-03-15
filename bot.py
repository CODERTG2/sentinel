import discord
from discord.ext import commands

token = "MTIxODMxMTQ2NzExMjA3NTM3NQ.G1PQG_.nQmH72Gz26v0J_9mzj3OOTz8AWgxP7AHs8TxAo"

prefix = '$'

intents = discord.Intents.all()
client = commands.Bot(command_prefix=prefix, intents=intents)
client.remove_command("help")
client.command_prefix = prefix


@client.event
async def on_ready():
    guild_count = 0

    for guild in client.guilds:
        print(f"- {guild.id} (name: {guild.name})")

        guild_count = guild_count + 1

    print("SampleDiscordBot is in " + str(guild_count) + " guilds.")


@client.event
async def on_message(message):
    if message.content == "hello":
        await message.channel.send("hey dirtbag")


client.run(token)
