# coding: utf-8
from collections import OrderedDict

from sqlalchemy import Column, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# django と分離したいけど諦め
from .django import analyze_model

db_types = [
    'postgresql', 'mysql', 'oracle', 'sqlite', 'firebird', 'mssql',
    'default',  # don't move it
]
Base = declarative_base()
existing = {}


def declare(django_model, db=None, back_type=None):
    model_info = analyze_model(django_model)
    if django_model in existing:
        return existing[django_model]

    row_kwargs = OrderedDict({'__tablename__': model_info['table_name']})
    for name, field in model_info['fields'].items():
        col_types = {
            (db_type if db_type + '_type' in field else 'default'): field.pop(db_type + '_type', {})
            for db_type in db_types
        }
        col_type_options = {
            (db_type if db_type + '_type_option' in field else 'default'): field.pop(db_type + '_type_option', {})
            for db_type in db_types
        }
        type_key = db if db in col_types else 'default'
        col_type = col_types.get(type_key)
        col_type_option = col_type_options.get(type_key, {})

        rel_option = field.pop('rel_option', None)
        if col_type:
            col_args = [col_type(**col_type_option)]
            if 'fk_option' in field:
                col_args.append(ForeignKey(**field.pop('fk_option', {})))

            row_kwargs[name] = Column(*col_args, **field)

        if rel_option:
            if 'secondary' in rel_option:
                rel_option['secondary'] = declare(rel_option['secondary'])
            
            if 'logical_name' in rel_option:
                name = rel_option.pop('logical_name')

            back = rel_option.pop('back', None)
            if back and back_type:
                rel_option[back_type] = back

            row_kwargs[name] = relationship(rel_option.pop('target'), **rel_option)

    cls = existing[django_model] = type(model_info['table_name'], (Base,), row_kwargs)
    return cls

