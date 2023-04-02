import string
from sqlite3 import Connection, Cursor
from karas.box import MessageChain
from karas.event import Auto_Switch_Event
from datetime import datetime
from typing import List, Tuple, Dict, Union, Optional
import json


class MetaTable(type):
    def __new__(mcs, name: str, bases: Tuple, attrs: Dict):
        if bases:
            if "table" not in attrs:
                attrs["table"] = string.capwords(name)
            print(name, bases, attrs)
            print(bases[0].__dict__)
        return super().__new__(mcs, name, bases, attrs)


class Table(metaclass=MetaTable):
    table: str

    def __init__(self, conn: Connection, bot_id: int):
        self._conn = conn
        self._check_exists()
        self.bot_id = bot_id

    conn: Connection = property(lambda self: self._conn, ..., ...)

    def _check_exists(self):
        with self.conn.cursor() as _cursor:
            _cursor.execute(f"""create table {self.table}
    (
        id      integer not null
            constraint {self.table}_pk
                primary key autoincrement,
        dt      integer not null,
        sender  integer not null,
        target  integer not null,
        content TEXT    not null
    );
    """)
        self.conn.commit()

    def record(self, message: Union[Dict, MessageChain], is_self: bool = False, target: Optional[int] = None):
        if is_self:
            dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            sender = self.bot_id
            raw = message.raw
        else:
            msg = Auto_Switch_Event.parse_json(**message)
            target = msg.group.id if msg.type == "GroupMessage" else self.bot_id
            sender = msg.sender.id
            dt = datetime.fromtimestamp(msg.messageChain.fetchone("Source").time).strftime("%Y-%m-%d %H:%M:%S")
            raw = msg.raw
        with self.conn.cursor() as _cursor:
            sql = f"insert into {self.table}(dt,sender,target,raw_message) values {dt, sender, target, json.dumps(raw, ensure_ascii=False)} "
            _cursor.execute(sql)
        self.conn.commit()

    def sync(self, message: Dict):
        msg = Auto_Switch_Event.parse_json(**message)
        dt = datetime.fromtimestamp(msg.messageChain.fetchone("Source").time).strftime("%Y-%m-%d %H:%M:%S")
        sender = self.bot_id
        target = msg.subject.id
        raw = msg.raw
        with self.conn.cursor() as _cursor:
            sql = f"insert into {self.table}(dt,sender,target,raw_message) values {dt, sender,target,json.dumps(raw,ensure_ascii=False)}"
            _cursor.execute(sql)
        self.conn.commit()


class GroupMessages(Table):
    table = "GroupMessages"


class FriendMessages(Table):
    table = "FriendMessages"


class TempMessages(Table):
    table = "TempMessages"


class StrangerMessages(Table):
    table = "StrangerMessages"
