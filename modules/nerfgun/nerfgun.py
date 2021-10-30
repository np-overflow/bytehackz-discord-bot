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


class Nerfgun(Scale):
    def __init__(self, bot):
        self.bot = bot
        self.queueMsg = None
        self.queue = []
        self.next = None

    @slash_command("nerf_setup", "Setup the Nerf Gun queue in a specified text channel")
    @slash_option(
        "channel",
        "ChannelID of channel to set up queue",
        OptionTypes.CHANNEL,
        required=True,
    )
    async def nerf_setup(self, ctx: InteractionContext, channel):

        if type(channel) != GuildText:
            await ctx.send(
                embeds=[
                    Embed("Whoops", f"Channel must be a text channel", color="#F9AC42")
                ]
            )
            return

        await channel.purge()

        embed = Embed(
            "Nerf R' Us 🔫",
            "Let's face it, programming 🖥, *is hard*. So while you're racking your brains working on prototypes, remember to take breathers!\n\n\
            In fact, if you're up for destressing, come on down to **Nerf R' Us**!\n\n \
            Here, you'll get to wield **heavily modded**, *high calibre* weaponary* in a simple but fun game of can shooting 🎯\n\n\n\
            At the end of the day, individuals/pairs with the highest scores get a special prize! 👀\n\n\n\
            We're located south of the Green Patch, queue up with the bot and we'll ping ya when you can come! 📍\n\n\
            Weaponary include:",
            color="#F9AC42",
            footer="*no actual weapons lah, just nerf guns",
            image="https://cdn.discordapp.com/attachments/900759773178396785/903654583845417040/bytehackz2021.003.png",
        )
        embed.add_field("item", "desc")
        embed.add_field("item", "desc")

        await channel.send(embeds=[embed])

        self.queueMsg = await channel.send("The queue is empty")

        button1 = Button(
            style=ButtonStyles.BLURPLE,
            label="Queue up",
            emoji="▶",
            custom_id="getInQueue",
        )  # Camel case good, dont @ me

        button2 = Button(
            style=ButtonStyles.RED,
            label="De-queue",
            custom_id="getOutQueue",
        )

        await channel.send(
            "Wanna give it a try? Click here and we'll give u a direct ping when you're up!",
            components=[button1, button2],
        )

        await ctx.send("Queue setup complete")

    @slash_command("nerf_next", "Call up the next individual in the queue")
    async def nerf_next(self, ctx: InteractionContext):
        if len(self.queue) == 0:
            await ctx.send("Queue currently empty!", ephemeral=True)
            return

        self.queue.pop(0)
        await self.update_queue()
        await ctx.send(f"Queue updated, {len(self.queue)} in queue", ephemeral=True)

    async def update_queue(self):
        if self.queueMsg is None:
            return

        if len(self.queue) == 0:
            await self.queueMsg.edit("The queue is currently empty!")
            return

        text = "\n\n```\n"
        for index, user in enumerate(self.queue):
            u = await self.bot.get_user(user)
            text += f"{index + 1}. {u.display_name}\n"
        text += "```\n\n"

        await self.queueMsg.edit(text)

        if len(self.queue) == 0:
            self.next = None
            return

        user = await self.bot.get_user(self.queue[0])

        if user.id == self.next:
            return

        await user.send(f"Hey {user.display_name}, you're up for the NERF game, be here in 5 mins or we'll move on!")

    @component_callback("getInQueue")
    async def get_in_queue(self, ctx):
        author = ctx.author

        if author.id in self.queue:
            await ctx.send("You're already in the queue mate", ephemeral=True)
            return

        self.queue.append(author.id)
        await self.update_queue()
        await ctx.send("Queue up successful! Wait for our ping!", ephemeral=True)

    @component_callback("getOutQueue")
    async def get_out_queue(self, ctx):
        author = ctx.author

        if author.id in self.queue:
            self.queue.remove(author.id)
            await ctx.send("De-queued you", ephemeral=True)
            await self.update_queue()
            return
        pass


def setup(bot):
    Nerfgun(bot)
