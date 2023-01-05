import string
from sqlite3 import Connection, connect


class MetaTable(type):
    def __new__(mcs, name, bases, attrs):
        if bases:
            if "table" not in attrs:
                attrs["table"] = string.capwords(name)
        return super().__new__(mcs, name, bases, attrs)


class Table(metaclass=MetaTable):
    def __init__(self, conn: Connection, *args, **kwargs):
        self._conn = conn

    conn: Connection = property(lambda self: self._conn, ..., ...)

    def __call__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class GroupMessages(Table):
    # table = "GroupMessages"
    field1: str = "123"
