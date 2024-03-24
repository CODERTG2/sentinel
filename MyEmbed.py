import discord


class MyEmbed(discord.Embed):
    def __init__(self, title, description, **kwargs):
        super().__init__(title=title,
                         description=description,
                         color=0xeabfff,
                         **kwargs)