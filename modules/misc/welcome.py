from typing import Type
from dis_snek.models import Scale
from dis_snek.models.application_commands import (
    OptionTypes,
    slash_command,
    slash_option,
)
from dis_snek.models.command import message_command
from dis_snek.models.context import InteractionContext
from dis_snek.models.discord_objects.embed import EmbedAttachment
from dis_snek.models.discord_objects.embed import Embed


class Welcome(Scale):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="welcome", description="It's time for Bytehackz 2021!")
    async def welcome(self, ctx: InteractionContext):
        embed = Embed(
            "Hello and welcome to Bytehackz 2021!",
            "The Byte®Hackz is an annual hackathon conducted for the Information Technology and Financial Informatics students taking the module Portfolio Development (PFD).\n\n\
            There will be 8 challenge statements, with 5 Groups of 4 to 5 Participants attempting each challenge statement.",
            color="#F9AC42"
            )

        await ctx.send(embeds=[embed])
    
        await ctx.send("https://cdn.discordapp.com/attachments/895590724836401175/904702785965150278/unknown.png")

            
def setup(bot):
    Welcome(bot)
