from pathlib import Path

import attr
import orjson
from dis_snek.mixins.serialization import DictSerializationMixin

from storage.genius import Genius
from storage.nerf import Nerf


@attr.s(slots=True)
class Container(DictSerializationMixin):
    nerf: Nerf = attr.ib(factory=dict, converter=Nerf.from_dict)
    genius: Genius = attr.ib(factory=dict, converter=Genius.from_dict)


class JsonStorage:
    def __init__(self, bot, filename: str):
        self.bot = bot
        self.filename = Path(filename)
        self.container = None
        self._init_data()

    def _init_data(self):
        if self.filename.is_file():
            with open(self.filename, "r") as file:
                data = orjson.loads(file.read())
                self.container = Container.from_dict(data)
        else:
            self.container = Container()

    def save(self):
        with open(self.filename, "wb") as file:
            data = orjson.dumps(self.container.to_dict())
            file.write(data)
