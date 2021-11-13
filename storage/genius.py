from typing import List, Any, Dict, Union

import attr
from dis_snek.mixins.serialization import DictSerializationMixin
from dis_snek.models import to_snowflake_list, User, Member


@attr.s(slots=True)
class Genius(DictSerializationMixin):
    queue: List[int] = attr.ib(factory=list, converter=to_snowflake_list)
    active: List[int] = attr.ib(factory=list, converter=to_snowflake_list)

    async def load_discord_objects(self, bot):
        pass

    def enqueue(self, user: Union[User, Member]):
        self.queue.append(user.id)

    def dequeue(self) -> int:
        return self.queue.pop(0)
