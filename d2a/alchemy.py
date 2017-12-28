# coding: utf-8
from collections import OrderedDict

from sqlalchemy import (
    Column,
    ForeignKey,
    types as common_types
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import postgresql as postgresql_types
from sqlalchemy.orm import relationship


Base = declarative_base()

types = {
    'int': common_types.INT,
    'smallint': common_types.SmallInteger,
    'bigint': common_types.BigInteger,
    'char': common_types.CHAR,
    'varchar': common_types.VARCHAR,
    'text': common_types.Text,
    'boolean': common_types.Boolean,
    'time': common_types.Time,
    'date': common_types.Date,
    'datetime': common_types.DateTime,
    'uuid': postgresql_types.UUID,
    'inet': postgresql_types.INET,
    'interval': postgresql_types.INTERVAL,
    'binary': common_types.Binary,
    'bytea': postgresql_types.BYTEA,
}

existing_tables = {}


def declare(model_info, db=None, back_type=None):
    table_name = model_info['name']
    if table_name in existing_tables:
        return existing_tables[table_name]

    secondaries = {}
    cls_kwargs = OrderedDict({'__tablename__': table_name})
    for name, field in model_info['fields'].items():
        if 'secondary' in field:
            field_name = field['secondary']['name']
            table = secondaries.get(field_name, declare(field['secondary']))
            kwargs = {back_type: field['related_name']} if back_type else {}
            cls_kwargs[name] = relationship(field_name, secondary=table, **kwargs)
            continue

        args = [name]
        key = field['type']
        if isinstance(key, dict):
            key = key.get(db, key['default'])
        atype = types[key]
        if key in {'char', 'varchar'}:
            atype = atype(field['length'])
        args += [atype]
        if 'related_to' in field:
            args += [ForeignKey(field['related_to'], ondelete=field.get('on_delete'))]
        kwargs = {k: field[k] for k in ['primary_key', 'unique', 'nullable', 'default']}
        cls_kwargs[name] = Column(*args, **kwargs)

    cls = existing_tables[table_name] = type(table_name, (Base,), cls_kwargs)
    return cls

