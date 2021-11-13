from typing import List, Any, Dict, Union

import attr
from dis_snek.mixins.serialization import DictSerializationMixin
from dis_snek.models import to_snowflake_list, User, Member, to_snowflake


@attr.s(slots=True)
class Genius(DictSerializationMixin):
    queue: List[int] = attr.ib(factory=list, converter=to_snowflake_list)
    occupied: Dict[str, int] = attr.ib(factory=dict)

    async def load_discord_objects(self, bot):
        pass

    @property
    def queue_msg(self):
        return

    def enqueue(self, user: Union[User, Member]):
        self.queue.append(user.id)

    def dequeue(self) -> int:
        return self.queue.pop(0)

    def new_ticket(self, user, category):
        self.occupied[str(to_snowflake(user))] = to_snowflake(category)

    def close_ticket(self, user):
        return self.occupied.pop(str(to_snowflake(user)))
