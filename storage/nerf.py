from typing import List, Dict, Any, Union, Optional

import attr
from attr.converters import optional
from dis_snek import Snake
from dis_snek.mixins.serialization import DictSerializationMixin
from dis_snek.models import to_snowflake_list, Member, User, to_snowflake, Message, ClientObject
from dis_snek.utils.serializer import no_export_meta

from utils.config import GUILD


@attr.s(slots=True)
class Nerf(DictSerializationMixin):
    queue: List[int] = attr.ib(factory=list, converter=to_snowflake_list)
    score: Dict[str, int] = attr.ib(factory=dict)
    queue_msg_channel: Optional[int] = attr.ib(default=None, converter=optional(to_snowflake))
    queue_msg_id: Optional[int] = attr.ib(default=None, converter=optional(to_snowflake))
    leaderboard_msg_channel: Optional[int] = attr.ib(default=None, converter=optional(to_snowflake))
    leaderboard_msg_id: Optional[int] = attr.ib(default=None, converter=optional(to_snowflake))

    _queue_msg: Message = attr.ib(default=None, metadata=no_export_meta)
    _leaderboard_msg: Message = attr.ib(default=None, metadata=no_export_meta)

    async def load_discord_objects(self, bot):
        guild = await bot.get_guild(GUILD)
        if self.queue_msg_channel and self.queue_msg_id:
            channel = await guild.get_channel(self.queue_msg_channel)
            self._queue_msg = await channel.get_message(self.queue_msg_id)

        if self.leaderboard_msg_channel and self.leaderboard_msg_id:
            channel = await guild.get_channel(self.leaderboard_msg_channel)
            self._leaderboard_msg = await channel.get_message(self.leaderboard_msg_id)

    @property
    def queue_msg(self):
        return self._queue_msg

    @property
    def leaderboard_msg(self):
        return self._leaderboard_msg

    def set_queue_message(self, message: Message):
        self.queue_msg_channel = message.channel.id
        self.queue_msg_id = message.id
        self._queue_msg = message

    def set_leaderboard_message(self, message: Message):
        self.leaderboard_msg_channel = message.channel.id
        self.leaderboard_msg_id = message.id
        self._leaderboard_msg = message

    def is_setup_done(self):
        return self._leaderboard_msg and self._queue_msg

    def enqueue(self, user: Union[User, Member]):
        self.queue.append(to_snowflake(user))

    def dequeue(self) -> int:
        return self.queue.pop(0)

    def queue_is_empty(self):
        return len(self.queue) <= 0

    def set_score(self, user, score):
        self.score[str(to_snowflake(user))] = score
