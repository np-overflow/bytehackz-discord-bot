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

from storage.genius import Genius
from utils.config import GUILD, PARTICIPANT_ROLE, MAX_TICKETS
from utils.embeds import GENIUS_BAR


class GeniusBar(Scale):
    def __init__(self, bot):
        self.bot = bot
        self.maxTickets = MAX_TICKETS
        self.genius: "Genius" = bot.storage.container.genius


    @listen()
    async def on_ready(self):
        print(MAX_TICKETS)
        await self.genius.load_discord_objects(self.bot)
        if self.genius.is_setup_done():
            await self.update_queue()


    @slash_command(
        name="genius", 
        sub_cmd_name="setup",
        sub_cmd_description="Setup the Genius Bar in a text channel")
    @slash_option(
        "channel",
        "ChannelID of channel to set up Genius Bar",
        OptionTypes.CHANNEL,
        required=True)
    async def genius_setup(self, ctx: InteractionContext, channel):
        await ctx.defer()

        if type(channel) != GuildText:
            await ctx.send(embeds=[Embed("Whoops", f"Channel must be a text channel", color="#F9AC42")])
            return

        if self.genius.is_setup_done():
            await ctx.send(embeds=Embed("Whoops", f"You have already setup the genius bar channel!", color="#F9AC42"))
            return

        await self.setup_channel(channel)
        await self.update_queue()
        await ctx.send("Setup complete")


    @slash_command(
        name="genius", 
        sub_cmd_name="kill",
        sub_cmd_description="Kill all occupied and currently queued tickets")
    async def genius_kill(self, ctx):
        await ctx.defer()

        guild = await self.bot.get_guild(GUILD)
        self.genius.queue.clear()

        for i in self.genius.occupied:
            catId = self.genius.occupied[i]
            cat = await self.bot.get_channel(catId)
            channels = cat.channels

            for i in channels:
                await guild.delete_channel(i.id)
            await guild.delete_channel(cat)

        self.genius.occupied.clear()
        await ctx.send("Tickets cleared")
        self.bot.storage.save()


    async def setup_channel(self, channel):
        await channel.purge()
        await channel.send(embeds=[GENIUS_BAR])

        self.genius.occupied.clear()
        self.genius.queue.clear()
        queue_msg = await channel.send("Queue here")
        print(queue_msg)


        self.genius.set_queue_message(queue_msg)

        await channel.send(
            "Book a session here and we'll ping you when we're free!",
            components=[
                Button(style=ButtonStyles.BLURPLE, label="Queue up", emoji="▶", custom_id="getIn"), 
                Button(style=ButtonStyles.RED, label="De-queue", custom_id="getOut")
                ]
            )


    async def update_queue(self):
        text = "```\n"

        if self.genius.queue_empty():
            text += "The queue is currently empty!"
        else:
            for index, user in enumerate(self.genius.queue):
                u = await self.bot.get_user(user)
                text += f"{index + 1}. {u.display_name}\n"

        text += "```"

        await self.genius.queue_msg.edit(text)


    @component_callback("getIn")
    async def get_in_queue(self, ctx):
        if not self.genius.queue_msg:
            await ctx.send("Error: Queue channel not setup yet.", ephemeral=True)
            return

        author_id = ctx.author.id

        if str(author_id) in self.genius.occupied:
            await ctx.send("1 ticket at a time only please", ephemeral=True)
            return
        if author_id in self.genius.queue:
            await ctx.send("You're already queueing up!", ephemeral=True)
            return

        if len(self.genius.occupied) < MAX_TICKETS:
            await self.create_ticket(author_id)
            await ctx.send("Ticket created!", ephemeral=True)
        else: 
            self.genius.enqueue(ctx.author)
            await ctx.send("We're at capacity so we've queued you up! You'll get a ping when we're free! ;)", ephemeral=True)
        
        self.bot.storage.save()
        await self.update_queue()


    @component_callback("getOut")
    async def get_out_queueu(self, ctx: InteractionContext):
        if not self.genius.queue_msg:
            await ctx.send("Error: Queue channel not setup yet.", ephemeral=True)
            return

        author_id = ctx.author.id
        if author_id in self.genius.queue:
            self.genius.queue.remove(author_id)
            self.bot.storage.save()
            await ctx.send("De-queued you", ephemeral=True)
            await self.update_queue()
        else:
            await ctx.send("You are already not in the queue :(", ephemeral=True)


    @component_callback("closeTicket")
    async def close_ticket(self, ctx: InteractionContext):
        author_id = str(ctx.author.id)

        if author_id not in self.genius.occupied:
            await ctx.send("You did not create this ticket!", ephemeral=True)

        cat = self.genius.occupied[author_id]
        if cat != ctx.channel.parent_id: # shouldnt happen
            return

        guild = await self.bot.get_guild(GUILD)
        cat = await guild.get_channel(cat)
        channels = cat.channels

        for i in channels:
            await guild.delete_channel(i.id)
        await guild.delete_channel(cat)

        self.genius.close_ticket(author_id)

        if len(self.genius.queue) == 0: #no-one in queue
            self.bot.storage.save()
            await self.update_queue()
            return

        userId = self.genius.dequeue()
        await self.create_ticket(userId)
        self.bot.storage.save()
        await self.update_queue()


    async def create_ticket(self, userId):
        userName = (await self.bot.get_user(userId)).display_name
        guild = await self.bot.get_guild(GUILD)
        cat = await guild.create_category(
            f"ticket-{userName}",
            position=999)

        await cat.edit_permission(
            PermissionOverwrite(
                id=PARTICIPANT_ROLE,
                type=0, 
                deny="1024",
                allow="0"
            ))

        await cat.edit_permission(
            PermissionOverwrite(
                id=userId,
                type=1,
                allow="1024",
                deny="0"
            ))
        
        tc = await guild.create_text_channel(f"ticket-{userName}", category=cat.id)
        await guild.create_voice_channel(f"ticket-{userName}", category=cat.id)

        button3 = Button(
            style=ButtonStyles.RED,
            label="Close ticket",
            custom_id="closeTicket"
        )

        await tc.send(
            f"Hey <@{userId}>! Welcome to your support channel! Please explain your issue here and someone will help you shortly. Alternatively, join your assigned vc.", # This text was definitely not stolen ;)
            components=[button3]
            ) 

        self.genius.new_ticket(userId, cat.id)
        

def setup(bot):
    GeniusBar(bot)
