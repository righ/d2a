# coding: utf-8
from collections import OrderedDict

from django.db.models.base import ModelBase
from django.db.models.fields import NOT_PROVIDED
from django.db import models

from .fields import mapping
from .compat import M2MField


def get_m2m_fields(model):
    return {
        k: v for k, v in vars(model).items()
        if isinstance(v, M2MField)
    }


def parse_field(field):
    info = {}
    field_type = type(field)

    for django_attr, alchemy_attr in [
        ('primary_key', 'primary_key'), 
        ('unique', 'unique'), 
        ('null', 'nullable'),
    ]:
        if hasattr(field, django_attr):
            info[alchemy_attr] = getattr(field, django_attr)

    if getattr(field, 'default', NOT_PROVIDED) is not NOT_PROVIDED:
        info['default'] = field.default

    info.update(mapping[field_type])
    while '_callback' in info:
        result = info.pop('_callback')(field)
        if isinstance(result, tuple):
            result, field = result
        info.update(result)
    return info


def parse_model(model, callback=parse_field):
    info = {'table_name': model._meta.db_table, 'fields': OrderedDict()}
    for field in model._meta.fields:
        info['fields'][field.attname] = callback(field)

    for name, field in get_m2m_fields(model).items():
        info['fields'][name] = callback(field)

    return info


def parse_models(module):
    models = {}
    for name, model in [(name, getattr(module, name)) for name in dir(module)]:
        if isinstance(model, ModelBase) and not model._meta.abstract:
            models[name] = model
    return models
