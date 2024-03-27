import discord


class MyEmbed(discord.Embed):
    def __init__(self, title, description, **kwargs):
        super().__init__(title=title,
                         description=description,
                         color=0xeabfff,
                         **kwargs)

    async def my_add_field(self, *, key_value: dict, channel, inline=False):
        items = list(key_value.items())
        send_embed = self
        for i in range(0, len(items), 25):
            for key, value in items[i:i + 25]:
                send_embed.add_field(name=key, value=value, inline=inline)
            await channel.send(embed=send_embed)
            send_embed = MyEmbed(title=self.title, description=self.description)
