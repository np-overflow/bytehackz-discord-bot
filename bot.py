import logging
from pathlib import Path

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dis_snek.client import Snake
from dis_snek.errors import CommandCheckFailure
from dis_snek.mixins.send import SendMixin
from dis_snek.models import message_command, has_role, check
from dis_snek.models.application_commands import slash_command
from dis_snek.models.context import InteractionContext, MessageContext
from dis_snek.models.discord_objects.embed import Embed
from dis_snek.models.listener import listen

from storage.storage import JsonStorage
from utils.config import TOKEN, GUILD, BOT_DEV_ROLE, LOGGING_LEVEL


logging.basicConfig()
logger = logging.getLogger("dis.snek")
logger.setLevel(LOGGING_LEVEL)


class BytehackzBot(Snake):
    storage: JsonStorage  # Lazy way for type hinting working

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

    @listen()
    async def on_disconnect(self):
        self.storage.save()

    @message_command("sync")
    # @check(has_role(BOT_DEV_ROLE))
    async def sync(self, ctx: MessageContext):
        sync_msg = await ctx.send("Sync starting...")
        await bot.synchronise_interactions()
        await sync_msg.edit("Syncing done!")

    @message_command("data_download")
    # @check(has_role(BOT_DEV_ROLE))
    async def data_download(self, ctx: MessageContext):
        await ctx.send("Here is the data!", file=self.storage.filename)

    @slash_command("help", "Basic instructions and what this bot is.")
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


bot = BytehackzBot(default_prefix="!", debug_scope=GUILD, sync_interactions=True)

bot.storage = JsonStorage("data.json", "./backup", 20)
scheduler = AsyncIOScheduler()
scheduler.add_job(bot.storage.backup, 'interval', minutes=5)
scheduler.start()

bot.load_all_scales("modules")
bot.start(TOKEN)
