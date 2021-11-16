import datetime
import os
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
    def __init__(self, filename: str, backup_folder: str, max_backups=5):
        self.filename = Path(filename)
        self.backup_folder = Path(backup_folder)
        self.max_backups = max_backups
        self.container = None
        self._init_data()

    def _init_data(self):
        if self.filename.is_file():
            with open(self.filename, "r") as file:
                data = orjson.loads(file.read())
                self.container = Container.from_dict(data)
        else:
            self.container = Container()

        self.backup_folder.mkdir(exist_ok=True)

    def save(self):
        self._save_file(self.filename)

    def backup(self):
        backup_filename = f"backup-{datetime.datetime.now().timestamp()}.json"
        backup_path = self.backup_folder.joinpath(backup_filename)
        self._save_file(backup_path)

        backup_files = sorted(os.listdir(self.backup_folder), key=lambda file: os.path.getctime(self.backup_folder.joinpath(file).absolute()))
        if len(backup_files) > self.max_backups:
            os.remove(self.backup_folder.joinpath(backup_files[0]).absolute())

        print("Backup done")

    def _save_file(self, path):
        with open(path, "wb") as file:
            data = orjson.dumps(self.container.to_dict(), option=orjson.OPT_NON_STR_KEYS)
            file.write(data)
