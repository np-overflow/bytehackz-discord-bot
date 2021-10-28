import logging
from pathlib import Path

from dis_snek.client import Snake
from dis_snek.errors import CommandCheckFailure
from dis_snek.mixins.send import SendMixin
from dis_snek.models import message_command, has_role, check
from dis_snek.models.application_commands import slash_command
from dis_snek.models.context import InteractionContext, MessageContext
from dis_snek.models.discord_objects.embed import Embed
from dis_snek.models.listener import listen

from utils.config import TOKEN, GUILD, BOT_DEV_ROLE

logging.basicConfig()
logger = logging.getLogger("dis.snek")
logger.setLevel(logging.DEBUG)


class BytehackzBot(Snake):
    def load_all_scales(self, module: str, nested: bool = True):
        path = Path.cwd()
        for m in module.split("."):
            path = path.joinpath(m)

        for item in path.iterdir():
            if item.name.startswith("."):
                continue

            if item.is_dir() and nested:
                self.load_all_scales(f"{module}.{item.stem}", nested)
            elif item.is_file() and item.suffix == ".py":
                bot.grow_scale(f"{module}.{item.stem}")

    @listen()
    async def on_ready(self):
        print(f"Logged in as: {self.user}")
        print(f"Servers: {len(self.guilds)}")
        print(f"I am in: {[i.name for i in self.guilds]}")

    @message_command("sync")
    # @check(has_role(BOT_DEV_ROLE))  # TODO add this back soon
    async def sync(self, ctx: MessageContext):
        await bot.synchronise_interactions()
        await ctx.send("Syncing done!")

    @slash_command("help2", "Basic instructions and what this bot is.")
    async def help(self, ctx: InteractionContext):
        embed = Embed(
            "ByteHackz",
            "text",
            color="#F9AC42",
        )
        embed.add_field("topic1", "value")
        await ctx.send(embeds=[embed])

    async def on_command_error(self, source: str, error: Exception, *args, **kwargs) -> None:
        if isinstance(error, CommandCheckFailure) and isinstance(error.context, SendMixin):
            await error.context.send("You don't have permission to run this command.")
        else:
            await self.on_error(source, error, *args, **kwargs)


bot = BytehackzBot(default_prefix="!", debug_scope=GUILD)
bot.load_all_scales("modules")
bot.start(TOKEN)
