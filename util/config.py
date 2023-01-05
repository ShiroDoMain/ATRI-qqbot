from typing import Dict, Union, Tuple
from karas.box import BotProfile
from sqlite3 import Connection
import toml


class ConfigBase:
    def __init__(self, config: Dict):
        for k, v in config.items():
            setattr(self, k, v)


class BotConfig(ConfigBase, BotProfile):
    host: str
    port: int
    verifyKey: str
    qq: str
    master: int

    def setBotProfile(self, profile: BotProfile):
        for k, v in profile.raw.items():
            setattr(self, k, v)


class DirectoryConfig(ConfigBase):
    fonts: str
    stickers: str


class DatabaseConfig(ConfigBase):
    path: str


class _RecorderConfig(ConfigBase):
    enable: bool
    bot: bool
    sync: bool


class RecoderConfig:
    group_config: _RecorderConfig
    friend_config: _RecorderConfig
    temp_config: _RecorderConfig
    stranger_config: _RecorderConfig

    def __init__(self, config: Dict):
        self.group_config = _RecorderConfig(config.get("GroupMessage"))
        self.friend_config = _RecorderConfig(config.get("FriendMessage"))
        self.temp_config = _RecorderConfig(config.get("TempMessage"))
        self.stranger_config = _RecorderConfig(config.get("StrangerMessage"))



class Config:
    @staticmethod
    def load_config(file: str) -> Tuple[BotConfig, DirectoryConfig, DatabaseConfig, RecoderConfig]:
        config: Dict = toml.load(file)
        bot_config = BotConfig(config.get("Bot"))
        dir_config = DirectoryConfig(config.get("Dirs"))
        database_config = DatabaseConfig(config.get("Database"))
        recoder_config = RecoderConfig(config.get("Recorder"))

        return bot_config, dir_config, database_config, recoder_config
