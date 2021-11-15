from dis_snek.models.application_commands import Permission
from utils.config import BOT_DEV_ROLE, ADMIN_ROLE, PARTICIPANT_ROLE, GUILD

NOT_EVERYBODY = Permission(
    id=PARTICIPANT_ROLE,
    guild_id=GUILD,
    type=1,
    permission=False
)

ADMIN_ONLY = Permission(
    id=ADMIN_ROLE,
    guild_id=GUILD,
    type=1,
    permission=True

)

BOT_DEV_ONLY = Permission(
    id=BOT_DEV_ROLE,
    guild_id=GUILD,
    type=1,
    permission=True
)