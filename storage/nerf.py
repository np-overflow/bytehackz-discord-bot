from typing import List, Dict, Any, Union, Optional

import attr
from attr.converters import optional
from dis_snek import Snake
from dis_snek.mixins.serialization import DictSerializationMixin
from dis_snek.models import to_snowflake_list, Member, User, to_snowflake, Message, ClientObject
from dis_snek.utils.serializer import no_export_meta

from storage.object_store import MessageStore
from utils.config import GUILD


@attr.s(slots=True)
class Nerf(DictSerializationMixin):
    queue: List[int] = attr.ib(factory=list, converter=to_snowflake_list)
    score: Dict[str, int] = attr.ib(factory=dict)
    queue_message: MessageStore = attr.ib(factory=dict, converter=MessageStore.from_dict)
    leaderboard_message: MessageStore = attr.ib(factory=dict, converter=MessageStore.from_dict)

    async def load_discord_objects(self, bot):
        await self.queue_message.load(bot)
        await self.leaderboard_message.load(bot)

    @property
    def queue_msg(self):
        return self.queue_message.message

    @property
    def leaderboard_msg(self):
        return self.leaderboard_message.message

    def set_queue_message(self, message: Message):
        self.queue_message.set(message)

    def set_leaderboard_message(self, message: Message):
        self.leaderboard_message.set(message)

    def is_setup_done(self):
        return self.leaderboard_message and self.queue_message

    def enqueue(self, user: Union[User, Member]):
        self.queue.append(to_snowflake(user))

    def dequeue(self) -> int:
        return self.queue.pop(0)

    def queue_is_empty(self):
        return len(self.queue) <= 0

    def set_score(self, user, score):
        self.score[str(to_snowflake(user))] = score
