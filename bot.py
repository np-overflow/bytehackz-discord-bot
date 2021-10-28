import logging
from pathlib import Path

from dis_snek.client import Snake
from dis_snek.models import message_command
from dis_snek.models.application_commands import slash_command
from dis_snek.models.context import InteractionContext, MessageContext
from dis_snek.models.discord_objects.embed import Embed
from dis_snek.models.listener import listen

from utils.config import TOKEN, GUILD


logging.basicConfig()
logger = logging.getLogger("dis.snek")
logger.setLevel(logging.DEBUG)


bot = Snake(default_prefix="!", debug_scope=GUILD)


@listen()
async def on_ready():
    print(f"Logged in as: {bot.user}")
    print(f"Servers: {len(bot.guilds)}")
    print(f"I am in: {[i.name for i in bot.guilds]}")


@message_command("sync")
async def sync(ctx: MessageContext):
    await bot.synchronise_interactions()
    await ctx.send("Syncing done!")


@slash_command("help", "Basic instructions and what this bot is")
async def help(ctx: InteractionContext):
    embed = Embed(
        "ByteHackz",
        "text",
        color="#F9AC42",
    )
    embed.add_field("topic1", "value")
    await ctx.send(embeds=[embed])


def load_all_scales(module: str, nested: bool = True):
    path = Path.cwd()
    for m in module.split("."):
        path = path.joinpath(m)

    for item in path.iterdir():
        if item.name.startswith("."):
            continue

        if item.is_dir() and nested:
            load_all_scales(f"{module}.{item.stem}", nested)
        elif item.is_file() and item.suffix == ".py":
            bot.grow_scale(f"{module}.{item.stem}")


load_all_scales("modules")


bot.start(TOKEN)
