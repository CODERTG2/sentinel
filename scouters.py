import importlib


async def set_scouters(ctx, arg):
    """Command to set the scouters for the competition"""
    client = importlib.import_module('main').client

    global scouters
    scouters = arg.split(",")
    await ctx.send("Scouters Set!")


async def assign_pit(ctx):
    """Command to assign pit scouting to scouters"""
    client = importlib.import_module('main').client

    for scout in scouters:
        pass
    await ctx.send("Pit Scouting Schedule Set!")


async def assign_match(ctx):
    """Command to assign match scouting to scouters"""
    client = importlib.import_module('main').client

    for scout in scouters:
        pass
    await ctx.send("Match Scouting Schedule Set!")
