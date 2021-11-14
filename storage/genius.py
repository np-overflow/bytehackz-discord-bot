from typing import List, Any, Dict, Union

import attr
from dis_snek.mixins.serialization import DictSerializationMixin
from dis_snek.models import to_snowflake_list, User, Member, to_snowflake, Message

from storage.object_store import MessageStore


@attr.s(slots=True)
class Genius(DictSerializationMixin):
    queue: List[int] = attr.ib(factory=list, converter=to_snowflake_list)
    occupied: Dict[str, int] = attr.ib(factory=dict)
    queue_message: MessageStore = attr.ib(factory=dict, converter=MessageStore.from_dict)

    async def load_discord_objects(self, bot):
        await self.queue_message.load(bot)

    @property
    def queue_msg(self):
        return self.queue_message.message

    def is_setup_done(self):
        return self.queue_message

    def set_queue_message(self, message: Message):
        self.queue_message.set(message)

    def enqueue(self, user: Union[User, Member]):
        self.queue.append(user.id)

    def dequeue(self) -> int:
        return self.queue.pop(0)

    def queue_empty(self):
        return len(self.queue) <= 0

    def new_ticket(self, user, category):
        self.occupied[str(to_snowflake(user))] = to_snowflake(category)

    def close_ticket(self, user) -> int:
        return self.occupied.pop(str(to_snowflake(user)))
