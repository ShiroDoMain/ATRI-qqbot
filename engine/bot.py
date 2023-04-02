import toml
from karas.box import Yurine
from util.config import load_config


class ATRIEngine:
    def __init__(self, botconfig, dirs, database, recorder):
        self.bot = Yurine(**botconfig)
        self.database = database
        self.dirs = dirs
        self.recorder = recorder

    @classmethod
    def load_config(cls):
        return cls(*load_config("config.toml"))
