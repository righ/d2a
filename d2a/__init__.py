# coding: utf-8
import re
from collections import OrderedDict

from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import relationship

from .parsers import parse_models, parse_model

db_types = ['postgresql', 'mysql', 'oracle', 'sqlite', 'firebird', 'mssql', 'default']
Base = declarative_base()
existing = {}


def declare(django_model, db=None, back_type=None):
    model_info = parse_model(django_model)
    if django_model in existing:
        return existing[django_model]

    row_kwargs = OrderedDict({'__tablename__': model_info['table_name']})
    for name, field in model_info['fields'].items():
        rel_option = field.pop('rel_option', None)

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

            column = row_kwargs[name] = Column(*col_args, **field)
            if rel_option is not None:
                rel_option['foreign_keys'] = [column]

        if rel_option:
            if 'secondary_model' in rel_option:
                secondary_model = rel_option.pop('secondary_model')
                secondary = rel_option['secondary'] = declare(secondary_model, db=db, back_type=back_type).__table__
                target_field = rel_option.pop('target_field')
                remote_primary_field = rel_option.pop('remote_primary_field')
                remote_secondary_field = rel_option.pop('remote_secondary_field')
                rel_option['primaryjoin'] = row_kwargs[target_field] == getattr(secondary.c, remote_primary_field)
                rel_option['secondaryjoin'] = row_kwargs[target_field] == getattr(secondary.c, remote_secondary_field)
            
            if 'logical_name' in rel_option:
                name = rel_option.pop('logical_name')

            back = rel_option.pop('back', None)
            if back and back_type:
                rel_option[back_type] = back.rstrip('+')

            row_kwargs[name] = relationship(rel_option.pop('target'), **rel_option)

    cls = existing[django_model] = type(model_info['table_name'], (Base,), row_kwargs)
    return cls


def get_camelcase(s):
    rs = list(re.finditer(r'(?<=_)\w', s))
    for r in reversed(rs):
        s = s[:r.start()-1] + r.group(0).upper() + s[r.end():]
    return s


def transfer(models, exports, db=None, back_type=None, as_table=False, name_formatter=get_camelcase):
    for model in parse_models(models).values():
        declare(model, db=db, back_type=back_type)

    for django_model, alchemy_model in existing.items():
        if models.__name__ == django_model.__module__:
            exports[name_formatter(django_model._meta.object_name)] = alchemy_model.__table__ if as_table else alchemy_model

