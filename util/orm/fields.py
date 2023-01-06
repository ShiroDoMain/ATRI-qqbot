from typing import Dict, Tuple


class MetaField(type):
    def __new__(mcs, name: str, bases: Tuple["Field"], attrs: Dict):
        if bases:
            cls = bases[0]
            vars = tuple([])
            for var in cls.__annotations__:
                if var not in cls.__init__.__annotations__:
                    pass


class FieldBase:
    field_type: str = None
    def __init__(
            self,
            verbose_name=None,
            name=None,
            primary_key=False,
            max_length=None,
            unique=False,
            blank=False,
            null=False,
            db_index=False,
            rel=None,
            default=None,
            editable=True,
            serialize=True,
            unique_for_date=None,
            unique_for_month=None,
            unique_for_year=None,
            choices=None,
            help_text="",
            db_column=None,
            db_tablespace=None,
            auto_created=False,
            field_type = field_type
    ):
        self.name = name
        self.verbose_name = verbose_name  # May be set by set_attributes_from_name
        self._verbose_name = verbose_name  # Store original for deconstruction
        self.primary_key = primary_key
        self.max_length, self._unique = max_length, unique
        self.blank, self.null = blank, null
        self.remote_field = rel
        self.is_relation = self.remote_field is not None
        self.default = default
        self.editable = editable
        self.serialize = serialize
        self.unique_for_date = unique_for_date
        self.unique_for_month = unique_for_month
        self.unique_for_year = unique_for_year
        self.choices = choices
        self.help_text = help_text
        self.db_index = db_index
        self.db_column = db_column
        self._db_tablespace = db_tablespace
        self.auto_created = auto_created
        self.field_type = field_type



class Field(FieldBase):
    def __init__(self, *_, **kwargs):
        for k, v in kwargs.items():
            if k not in self.__annotations__:
                raise ValueError(f"cannot found property {k} for {self.__class__.__name__}")
            setattr(self, k, v)
        super().__init__(*kwargs)

    def __str__(self):
        pass


class IntegerField:
    field_type = "integer"

class CharField:
    field_type = "vchar"

class JsonField:
    def
class DateField:
    value: str

    @classmethod
    def now(cls):
        pass


