from typing import Optional

import attr
from attr.converters import optional
from dis_snek.mixins.serialization import DictSerializationMixin
from dis_snek.models import to_snowflake, Message


@attr.s(slots=True)
class MessageStore(DictSerializationMixin):
    guild_id: Optional[int] = attr.ib(default=None, converter=optional(to_snowflake))
    channel_id: Optional[int] = attr.ib(default=None, converter=optional(to_snowflake))
    message_id: Optional[int] = attr.ib(default=None, converter=optional(to_snowflake))

    _message: Optional[Message] = attr.ib(default=None, metadata={"no_export": True})

    def __bool__(self):
        return self._message is not None

    @property
    def message(self):
        return self._message

    async def load(self, bot):
        if self.guild_id and self.channel_id and self.message_id:
            guild = await bot.get_guild(self.guild_id)
            channel = await guild.get_channel(self.channel_id)
            self._message = await channel.get_message(self.message_id)

    def set(self, message: Message):
        self.guild_id = message.guild.id
        self.channel_id = message.channel.id
        self.message_id = message.id
        self._message = message

    def delete(self):
        self.guild_id = None
        self.channel_id = None
        self.message_id = None
        self._message = None
