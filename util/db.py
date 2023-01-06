import string
from sqlite3 import Connection, connect, Cursor
from orm.fields import Field
from typing import List, Tuple, Dict


class MetaTable(type):

    def _build_sql(cls, operate: str, *values: List[Field]):
        pass

    def _check_exists(cls: "Table"):
        _cursor: Cursor = cls.conn.cursor()
        _cursor.execute("if ")

    def __new__(mcs, name: str, bases: Tuple["Table"], attrs: Dict):
        if bases:
            if "table" not in attrs:
                attrs["table"] = string.capwords(name)
            print(name, bases, attrs)
            print(bases[0].__dict__)
        return super().__new__(mcs, name, bases, attrs)


class Table(metaclass=MetaTable):
    def __init__(self, conn: Connection, *args, **kwargs):
        self._conn = conn
        print(self.__annotations__)

    conn: Connection = property(lambda self: self._conn, ..., ...)

    def __call__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class GroupMessages(Table):
    table = "GroupMessages"
    field1: str = "123"


gm = GroupMessages(conn="conn")
