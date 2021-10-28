from dis_snek.models import Scale
from dis_snek.models.application_commands import (
    OptionTypes,
    slash_command,
    slash_option,
)
from dis_snek.models.context import InteractionContext
from dis_snek.models.discord_objects.embed import EmbedAttachment
from dis_snek.models.discord_objects.embed import Embed

#IM SO SORRY YOU HAVE TO SEE THIS LINE OF CODE
codes = [100, 101, 102, 200, 201, 202, 203, 204, 206, 207, 300, 301, 302, 303, 304, 305, 307, 308, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 420, 421, 422, 423, 424, 425, 426, 429, 431, 444, 450, 451, 497, 498, 499, 500, 501, 502, 503, 504, 506, 507, 508, 509, 510, 511, 521, 523, 525, 599]

class Cat(Scale):
    def __init__(self, bot):
        self.bot = bot

    @slash_command("cat", "Get a (objectively) cute cat depending on your (mandatorily) provided status code", scopes=["895590724836401172"])
    @slash_option(
        "status_code",
        "The status code (or ID) of the cat you're lookin' for",
        OptionTypes.INTEGER,
        required=True
    )
    async def cat(self, ctx: InteractionContext, status_code: int = None):
        #this is a horrible way of doing this
        if not (status_code in codes):
            status_code = 404

        embed = Embed(
                    title=f"Code {status_code}",
                    description="Fetched u a Kat",
                    color="#B4DA55"
                )

        embed.image = EmbedAttachment(url=f"https://http.cat/{status_code}")

        await ctx.send(embeds=[embed])
        
def setup(bot):
    Cat(bot)
