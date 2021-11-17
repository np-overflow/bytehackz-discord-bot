from typing import Optional

from dis_snek.models import Scale, User, listen
from dis_snek.models.application_commands import (
    OptionTypes,
    component_callback,
    slash_command,
    slash_option,
    slash_permission
)
from dis_snek.models.context import InteractionContext
from dis_snek.models.discord_objects.channel import GuildText
from dis_snek.models.discord_objects.components import Button
from dis_snek.models.discord_objects.embed import Embed
from dis_snek.models.enums import ButtonStyles

from storage.nerf import Nerf
from utils.config import BOT_DEV_ROLE

from utils.embeds import NERF_GUN
from utils.perms import ADMIN_ONLY, BOT_DEV_ONLY, NOT_EVERYBODY


class Nerfgun(Scale):
    def __init__(self, bot):
        self.bot = bot
        self.nerf: "Nerf" = bot.storage.container.nerf
        self.now_playing_user: Optional["User"] = None

    @listen()
    async def on_ready(self):
        await self.nerf.load_discord_objects(self.bot)
        if self.nerf.is_setup_done():
            await self._update_queue()
            await self._update_leaderboard()

    @slash_command(
        name="nerf_setup",
        description="Setup the Nerf Gun queue in a specified text channel"
    )
    @slash_option(
        "queuechannel",
        "ChannelID of channel to set up queue",
        OptionTypes.CHANNEL,
        required=True,
    )
    @slash_option(
        "boardchannel",
        "ChannelID of channel to set up leaderboard",
        OptionTypes.CHANNEL,
        required=True,
    )
    @slash_permission(NOT_EVERYBODY, BOT_DEV_ONLY)
    async def nerf_setup(self, ctx: InteractionContext, queuechannel, boardchannel):
        await ctx.defer()

        if type(queuechannel) != GuildText or type(boardchannel) != GuildText:
            await ctx.send(embeds=Embed("Whoops", f"Channels must be text channels", color="#F9AC42"))
            return

        if self.nerf.is_setup_done():
            await ctx.send(embeds=Embed("Whoops", f"You have already setup the nerf channels!", color="#F9AC42"))
            return

        await self._setup_queue_channel(queuechannel)
        await self._setup_leaderboard_channel(boardchannel)
        self.bot.storage.save()

        await self._update_queue()
        await self._update_leaderboard()

        await ctx.send("Queue setup completed!")

    async def _setup_queue_channel(self, queuechannel):
        await queuechannel.purge()
        await queuechannel.send(embeds=[NERF_GUN])

        queue_msg = await queuechannel.send("Queue here!")
        self.nerf.queue.clear()
        self.nerf.set_queue_message(queue_msg)

        await queuechannel.send(
            "Wanna give it a try? Click here and we'll give u a direct ping when you're up!",
            components=[
                Button(
                    style=ButtonStyles.BLURPLE,
                    label="Queue up",
                    emoji="▶",
                    custom_id="getInQueue",
                ),
                Button(
                    style=ButtonStyles.RED,
                    label="De-queue",
                    custom_id="getOutQueue",
                )
            ],
        )

    async def _setup_leaderboard_channel(self, boardchannel):
        await boardchannel.purge()
        leaderboard_msg = await boardchannel.send("Leaderboard here!")
        self.nerf.score.clear()
        self.nerf.set_leaderboard_message(leaderboard_msg)

    @slash_command(
        name="nerf_next",
        description="Call up the next individual in the queue"
    )
    @slash_permission(NOT_EVERYBODY, ADMIN_ONLY)
    async def nerf_next(self, ctx: InteractionContext):
        if self.nerf.queue_is_empty():
            await ctx.send("Queue currently empty!")
            return

        if not self.nerf.queue_msg:
            await ctx.send("Please setup the nerf queue channel first!")
            return

        self.now_playing_user = await self.bot.get_user(self.nerf.dequeue())
        self.bot.storage.save()

        await self._update_queue()

        await ctx.send(f"It is now {self.now_playing_user}'s turn.")
        await self.now_playing_user.send(f"Hey {self.now_playing_user.display_name}! "
                                         f"You're up for the NERF game, be here in 5 mins or we'll move on!")

    @component_callback("getInQueue")
    async def get_in_queue(self, ctx):
        if not self.nerf.queue_msg:
            await ctx.send("Error: Queue channel not setup yet.", ephemeral=True)
            return

        author_id = ctx.author.id
        if author_id in self.nerf.queue:
            await ctx.send("You're already in the queue mate", ephemeral=True)
        else:
            self.nerf.enqueue(author_id)
            self.bot.storage.save()
            await self._update_queue()
            await ctx.send("Queue up successful! Wait for our ping!", ephemeral=True)

    @component_callback("getOutQueue")
    async def get_out_queue(self, ctx):
        if not self.nerf.queue_msg:
            await ctx.send("Error: Queue channel not setup yet.", ephemeral=True)
            return

        author_id = ctx.author.id
        if author_id in self.nerf.queue:
            self.nerf.queue.remove(author_id)
            self.bot.storage.save()
            await ctx.send("De-queued you", ephemeral=True)
            await self._update_queue()
        else:
            await ctx.send("You are already not in the queue :(", ephemeral=True)

    async def _update_queue(self):
        text = "\n\n```\nNow playing:"
        if self.now_playing_user:
            text += f"{self.now_playing_user.display_name}\n\n"
        else: 
            text += f"Nobody :(\n\n"
        
        if self.nerf.queue_is_empty():
            text += "\n\nThe queue is currently empty!"
        else:
            for index, user in enumerate(self.nerf.queue):
                u = await self.bot.get_user(user)
                text += f"{index + 1}. {u.display_name}\n"

        text += "```\n\n"

        await self.nerf.queue_msg.edit(text)

    @slash_command(
        name="nerf_score",
        description="Score a player"
    )
    @slash_option(
        "score",
        "The score you're giving this player (1-100)",
        OptionTypes.INTEGER,
        required=True
    )
    @slash_option(
        "player",
        "Player you're scoring, defaults to now playing user",
        OptionTypes.USER,
        required=False
    )
    @slash_permission(NOT_EVERYBODY, ADMIN_ONLY)
    async def nerf_score(self, ctx: InteractionContext, score, player = None):
        await ctx.defer()

        if score < 0 or score > 100:  # TODO Based it off the scoring system
            await ctx.send(embeds=Embed("Whoops", f"Score must be between 1 & 100", color="#F9AC42"))
            return

        if not player:
            player = self.now_playing_user

        self.nerf.set_score(player, score)
        self.bot.storage.save()

        await ctx.send(f"{player.display_name} scores {score} for the nerf game!")
        await self._update_leaderboard()

        if self.now_playing_user and player == self.now_playing_user:
            await self.now_playing_user.send(f"Thank you for playing, you scored {score}! Add yourself to queue to "
                                             f"play again!")
            self.now_playing_user = None

    async def _update_leaderboard(self):
        aggregated_scores = sorted(self.nerf.score.items(), key=lambda item: item[1], reverse=True)

        embed = Embed(
            "Nerf R' Us 🔫 **Leaderboard**",
            "Ranked by score:\n\n",
            color="#F9AC42",
            image="https://cdn.discordapp.com/attachments/900759773178396785/903654583845417040/bytehackz2021.003.png",
        )

        if len(aggregated_scores) >= 1:
            embed.add_field("1st place 🥇", f"<@{aggregated_scores[0][0]}> : {aggregated_scores[0][1]}", inline=True)
        else:
            embed.add_field("1st place 🥇", "N.A.", inline=True)

        if len(aggregated_scores) >= 2:
            embed.add_field("2nd place 🥈", f"<@{aggregated_scores[1][0]}> : {aggregated_scores[1][1]}", inline=True)
        else:
            embed.add_field("2nd place 🥈", "N.A.", inline=True)

        if len(aggregated_scores) >= 3:
            embed.add_field("3rd place 🥉", f"<@{aggregated_scores[2][0]}> : {aggregated_scores[2][1]}", inline=True)
        else:
            embed.add_field("3rd place 🥉", "N.A.", inline=True)

        runner_ups = ""
        for i in range(3, min(20, len(aggregated_scores))):
            runner_ups += f"{i+1} -> <@{aggregated_scores[i][0]}> : {aggregated_scores[i][1]}\n"
        if not runner_ups:
            runner_ups = "N.A."
        embed.add_field("Runner ups", runner_ups)

        await self.nerf.leaderboard_msg.edit(content="", embeds=embed)


def setup(bot):
    Nerfgun(bot)
