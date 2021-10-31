from dis_snek.models import Scale
from dis_snek.models.application_commands import (
    OptionTypes,
    component_callback,
    slash_command,
    slash_option,
)
from dis_snek.models.context import InteractionContext
from dis_snek.models.discord_objects.embed import EmbedAttachment, EmbedField
from dis_snek.models.discord_objects.components import Button, ActionRow
from dis_snek.models.discord_objects.channel import GuildText
from dis_snek.models.enums import ButtonStyles
from dis_snek.models.discord_objects.embed import Embed
from dis_snek.models.listener import listen


class Genius(Scale):
    def __init__(self, bot):
        self.bot = bot

    @slash_command("genius_setup", "Setup the Genius Bar in a text channel")
    @slash_option(
        "channel",
        "ChannelID of channel to set up Genius Bar",
        OptionTypes.CHANNEL,
        required=True)
    async def genius_setup(self, ctx: InteractionContext, channel):

        if type(channel) != GuildText:
            await ctx.send(embeds=[Embed(
                "Whoops",
                f"Channel must be a text channel",
                color="#F9AC42")])
            return
        
        await channel.purge()

        embed = Embed(
            "Genius Bar 🧠",
            "**Picture this**:\n\n\
            You've got yourself a cool prototype in mind, and as your Team is setting things up, you realize something.\n\n\
            Maybe its the fact that the services you're planning to use are incompaitable, or that Python 2.9 just won't cut it.\n\n\
            That's where the Techies over at the **Genius Bar** come into play!\n\n\
            These guys here have great experience and can offer valuable feedback and suggestions on how you can get your prototype up and running\n\n\n\
            To book a session, just click the button below! 👇",
            color="#F9AC42",
            footer="🧠",
            image="https://cdn.discordapp.com/attachments/900759773178396785/903654583845417040/bytehackz2021.003.png",
        )

        await channel.send(embeds=[embed])

        self.queueMsg = await channel.send("The queue is empty")

        button1 = Button(
            style=ButtonStyles.BLURPLE, 
            label="Queue up", emoji="▶",
            custom_id="getInQueue") #Camel case good, dont @ me

        button2 = Button(
            style=ButtonStyles.RED,
            label="De-queue",
            custom_id="getOutQueue"
        )

        await channel.send(
            "Book a session here and we'll ping you when we're free!",
            components=[button1, button2])

        await ctx.send("Queue setup complete")




def setup(Bot):
    Genius(Bot)
