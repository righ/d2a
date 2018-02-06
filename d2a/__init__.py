# coding: utf-8
from collections import OrderedDict

from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from .parsers import parse_models, parse_model
from .utils import get_camelcase
from .types import alias

db_types = ['postgresql', 'mysql', 'oracle', 'sqlite', 'firebird', 'mssql', 'default']
Base = declarative_base()
existing = {}


def declare(django_model, db=None, back_type=None):
    model_info = parse_model(django_model)
    if django_model in existing:
        return existing[django_model]

    rel_options = OrderedDict()
    rows = OrderedDict({'__tablename__': model_info['table_name']})
    for name, field in model_info['fields'].items():
        rel_option = field.pop('rel_option', {})
        if rel_option:
            rel_options[name] = rel_option

        col_types = {}
        col_type_options = {}
        for db_type in db_types:
            col_types[db_type] = field.pop(db_type + '_type', None)
            col_type_options[db_type] = field.pop(db_type + '_type_option', {})

        type_key = 'default' if col_types.get(db) is None else db
        if col_types[type_key]:
            col_args = [col_types[type_key](**col_type_options[type_key])]
            if 'fk_option' in field:
                col_args.append(ForeignKey(**field.pop('fk_option', {})))

            column = rows[name] = Column(*col_args, **field)
            rel_option['foreign_keys'] = [column]

    for logical_name, rel_option in rel_options.items():
        if 'secondary_model' in rel_option:
            secondary = rel_option['secondary'] = declare(rel_option.pop('secondary_model'), db=db, back_type=back_type).__table__
            target_field = rel_option.pop('target_field')
            rel_option['primaryjoin'] = rows[target_field] == secondary.c[rel_option.pop('remote_primary_field')]
            rel_option['secondaryjoin'] = rows[target_field] == secondary.c[rel_option.pop('remote_secondary_field')]
        
        if 'logical_name' in rel_option:
            logical_name = rel_option.pop('logical_name')

        back = rel_option.pop('back', None)
        if back and back_type:
            rel_option[back_type] = back.rstrip('+')

        rows[logical_name] = relationship(rel_option.pop('target'), **rel_option)

    cls = existing[django_model] = type(model_info['table_name'], (Base,), rows)
    return cls


def transfer(models, exports, db=None, back_type=None, as_table=False, name_formatter=get_camelcase):
    for model in parse_models(models).values():
        declare(model, db=db, back_type=back_type)

    for django_model, alchemy_model in existing.items():
        if models.__name__ == django_model.__module__:
            exports[name_formatter(django_model._meta.object_name)] = alchemy_model.__table__ if as_table else alchemy_model

