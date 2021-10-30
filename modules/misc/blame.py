from typing import Type
from dis_snek.models import Scale
from dis_snek.models.application_commands import (
    OptionTypes,
    slash_command,
    slash_option,
)
from dis_snek.models.context import InteractionContext
from dis_snek.models.discord_objects.embed import EmbedAttachment
from dis_snek.models.discord_objects.embed import Embed


class Blame(Scale):
    def __init__(self, bot):
        self.bot = bot

    @slash_command("blame", "Lmao")
    async def blame(self, ctx: InteractionContext):
        embed = Embed(
            "XD",
            color="#F9AC42",
            image="https://cdn.discordapp.com/attachments/903207401623281676/903895467522408458/blame.png",
        )

        await ctx.send(embeds=[embed])


def setup(bot):
    Blame(bot)
