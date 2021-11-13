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
from dis_snek.models.discord_objects.channel import GuildText, PermissionOverwrite
from dis_snek.models.discord_objects.guild import Guild
from dis_snek.models.enums import ButtonStyles
from dis_snek.models.discord_objects.embed import Embed
from dis_snek.models.listener import listen
from dis_snek.http_requests.channels import ChannelRequests

from utils.config import GUILD, PARTICIPANT_ROLE, MAX_TICKETS
from utils.embeds import GENIUS_BAR


class Genius(Scale):
    def __init__(self, bot):
        self.bot = bot
        self.occupied = {}
        self.queue = []
        self.maxTickets = MAX_TICKETS


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

        await channel.send(embeds=[GENIUS_BAR])

        self.queueMsg = await channel.send("The queue is empty")

        button1 = Button(
            style=ButtonStyles.BLURPLE, 
            label="Queue up", emoji="▶",
            custom_id="getIn")

        button2 = Button(
            style=ButtonStyles.RED,
            label="De-queue",
            custom_id="getOut")

        await channel.send(
            "Book a session here and we'll ping you when we're free!",
            components=[button1, button2])

        await ctx.send("Queue setup complete")


    @component_callback("getIn")
    async def get_in(self, ctx):
        user: int = ctx.author.id

        if user in self.occupied or user in self.queue:
            await ctx.send("Only 1 ticket at a time please!!", ephemeral=True)
            return

        if len(self.occupied) > self.maxTickets:
            self.queue.append(user)
            await ctx.send("We're at our limit at the moment, we've queued you up and will give you a ping when we're ready!", ephemeral=True)
            return

        await self.create_ticket(user)

        await ctx.send("Ticket created!", ephemeral=True)


    @component_callback("closeTicket")
    async def close_ticket(self, ctx: InteractionContext):
        channels = self.occupied[ctx.author.id]
        if channels[0] != ctx.channel.id: # User did not create ticket
            return

        g: Guild = await self.bot.get_guild(GUILD)
            
        await g.delete_channel(channels[0])
        await g.delete_channel(channels[1])
        await g.delete_channel(channels[2])

        self.occupied.pop(ctx.author.id , None)

        if len(self.queue) == 0: #no-one in queue
            return

        await self.create_ticket(self, self.queue[0])


    async def create_ticket(self, user):
        g: Guild = await self.bot.get_guild(GUILD)
        cat = await g.create_category(
            f"ticket-{user}",
            position=999)

        await cat.edit_permission(PermissionOverwrite(
                    id=PARTICIPANT_ROLE,
                    type=0,
                    deny="1024",
                    allow="0"
                ))

        await cat.edit_permission(PermissionOverwrite(
                    id=user,
                    type=1,
                    allow="1024",
                    deny="0"
                ))
        
        tc = await g.create_text_channel(
            f"ticket-{user}",
            category=cat.id
        )
        vc = await g.create_voice_channel(
            f"ticket-{user}",
            category=cat.id
        )

        self.occupied[user] = (tc.id, vc.id, cat.id)

        button3 = Button(
            style=ButtonStyles.RED,
            label="Close ticket",
            custom_id="closeTicket"
        )

        await tc.send(
            f"Hey <@{user}>! Welcome to your support channel! Please explain your issue here and someone will help you shortly. Alternatively, join your assigned vc.", # This text was definitely not stolen ;)
            components=[button3]
            ) 
        

def setup(Bot):
    Genius(Bot)
