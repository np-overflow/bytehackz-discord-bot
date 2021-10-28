import logging

from dis_snek.client import Snake
from dis_snek.models.application_commands import slash_command
from dis_snek.models.context import InteractionContext
from dis_snek.models.discord_objects.embed import Embed
from dis_snek.models.listener import listen

from utils.config import TOKEN, GUILD


logging.basicConfig()
logger = logging.getLogger("dis.snek")
logger.setLevel(logging.DEBUG)


bot = Snake(sync_interactions=True, debug_scope=GUILD)


@listen()
async def on_ready():
    print(f"Logged in as: {bot.user}")
    print(f"Servers: {len(bot.guilds)}")
    print(f"I am in: {[i.name for i in bot.guilds]}")


@slash_command("help", "Basic instructions and what this bot is")
async def help(ctx: InteractionContext):
    embed = Embed(
        "ByteHackz",
        "text",
        color="#F9AC42",
    )
    embed.add_field("topic1", "value")
    await ctx.send(embeds=[embed])


bot.grow_scale("modules.misc.httpcats")


bot.start(TOKEN)
