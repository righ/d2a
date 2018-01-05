# coding: utf-8
import re
from collections import OrderedDict

from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .parser import parse_models, parse_model

db_types = [
    'postgresql', 'mysql', 'oracle', 'sqlite', 'firebird', 'mssql',
    'default',  # don't move it
]
Base = declarative_base()
existing = {}


def declare(django_model, db=None, back_type=None):
    model_info = parse_model(django_model)
    if django_model in existing:
        return existing[django_model]

    row_kwargs = OrderedDict({'__tablename__': model_info['table_name']})
    for name, field in model_info['fields'].items():
        rel_option = field.pop('rel_option', None)
        if rel_option:
            if 'secondary' in rel_option:
                rel_option['secondary'] = declare(rel_option['secondary'])
            
            if 'logical_name' in rel_option:
                name = rel_option.pop('logical_name')

            back = rel_option.pop('back', None)
            if back and back_type:
                rel_option[back_type] = back

            row_kwargs[name] = relationship(rel_option.pop('target'), **rel_option)

        col_types = {}
        col_type_options = {}
        for db_type in db_types:
            if db_type + '_type' in field:
                col_types[db_type] = field.pop(db_type + '_type')
            if db_type + '_type_option' in field:
                col_type_options[db_type] = field.pop(db_type + '_type_option')

        type_key = db if db in col_types else 'default'
        if type_key in col_types:
            col_args = [col_types[type_key](**col_type_options.get(type_key, {}))]
            if 'fk_option' in field:
                col_args.append(ForeignKey(**field.pop('fk_option', {})))

            row_kwargs[name] = Column(*col_args, **field)

    cls = existing[django_model] = type(model_info['table_name'], (Base,), row_kwargs)
    return cls


def get_camelcase(s):
    rs = list(re.finditer(r'(?<=_)\w', s))
    for r in reversed(rs):
        s = s[:r.start()-1] + r.group(0).upper() + s[r.end():]
    return s


def transfer(models, exports, db=None, back_type=None, name_formatter=get_camelcase):
    for model in parse_models(models).values():
        declare(model, db=db, back_type=back_type)

    for django_model, alchemy_model in existing.items():
        if models.__name__ == django_model.__module__:
            exports[name_formatter(django_model._meta.object_name)] = alchemy_model

