from typing import Dict, Union, Tuple
from karas.box import BotProfile
from sqlite3 import Connection, connect
import toml


class ConfigBase:
    def __init__(self, config: Dict):
        for k, v in config.items():
            setattr(self, k, v)


class BotConfig(ConfigBase, BotProfile):
    host: str
    port: int
    verifyKey: str
    account: int
    loggerLevel: str
    logToFile: bool
    logRecordLevel: str

    @property
    def raw_conf(self):
        return {
            "host": self.host,
            "port": self.port,
            "verifyKey": self.verifyKey,
            "account": self.account,
            "loggerLevel": self.loggerLevel,
            "logToFile": self.logToFile,
            "logRecordLevel": self.logRecordLevel,
        }

    def setBotProfile(self, profile: BotProfile):
        for k, v in profile.raw.items():
            setattr(self, k, v)


class DirectoryConfig(ConfigBase):
    fonts: str
    stickers: str


class DatabaseConfig(ConfigBase):
    path: str

    def connect(self):
        return connect(self.path)


class _RecorderConfig(ConfigBase):
    enable: bool
    bot: bool
    sync: bool


class RecoderConfig:
    group: _RecorderConfig
    friend: _RecorderConfig
    temp: _RecorderConfig
    stranger: _RecorderConfig

    def __init__(self, config: Dict):
        self.group = _RecorderConfig(config.get("GroupMessage"))
        self.friend = _RecorderConfig(config.get("FriendMessage"))
        self.temp = _RecorderConfig(config.get("TempMessage"))
        self.stranger = _RecorderConfig(config.get("StrangerMessage"))


def load_config(file: str) -> Tuple[BotConfig, DirectoryConfig, DatabaseConfig, RecoderConfig]:
    config: Dict = toml.load(open(file))
    bot_config = BotConfig(config.get("Bot"))
    dir_config = DirectoryConfig(config.get("Dirs"))
    database_config = DatabaseConfig(config.get("Database"))
    recoder_config = RecoderConfig(config.get("Recorder"))

    return bot_config, dir_config, database_config, recoder_config
