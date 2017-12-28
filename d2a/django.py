# coding: utf-8
from collections import OrderedDict

from django.db.models.base import ModelBase
# The following fields are supported django 1.4 or later.
from django.db import models
# django >= 1.9
from django.db.models.fields.related_descriptors import ManyToManyDescriptor as M2MField

types = {
    models.AutoField: {'type': 'int'},
    models.IntegerField: {'type': 'int'},
    models.PositiveIntegerField: {'type': 'int'},
    models.SmallIntegerField: {'type': 'int'},
    models.PositiveSmallIntegerField: {'type': 'int', 'unsigned': True},
    models.BigIntegerField: {'type': 'bigint'},
    models.DecimalField: {'type': 'decimal',
                          'callback': lambda f: {'precision': f.max_digits, 'scale': f.decimal_places}},
    models.FloatField: {'type': 'float'},
    models.CharField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    models.SlugField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    models.URLField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    models.EmailField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    models.FileField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    models.FilePathField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    models.ImageField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    models.GenericIPAddressField: {'type': {'postgres': 'inet', 'default': 'char'},
                            'length': 39},

    models.BinaryField: {'postgres': 'bytea', 'default': 'binary'},
    models.DurationField: {'type': {'postgres': 'interval', 'default': 'bigint'}},
    models.UUIDField: {'type': {'postgres': 'uuid', 'default': 'char'}, 'length': 32},

    models.TextField: {'type': 'text'},
    models.DateTimeField: {'type': 'datetime'},
    models.DateField: {'type': 'date'},
    models.TimeField: {'type': 'time'},
    models.BooleanField: {'type': 'boolean'},
    models.NullBooleanField: {'type': 'boolean'},
    models.ForeignKey: {'callback': lambda f: {'on_delete': f.on_delete.__name__}},
    models.OneToOneField: {'callback': lambda f: {'on_delete': f.on_delete.__name__}},
}


def get_m2m_fields(model):
    return {
        k: v for k, v in vars(model).items()
        if isinstance(v, M2MField)
    }


try:
    # deprecated
    types[models.CommaSeparatedIntegerField] = {'type': 'varchar',
                                         'callback': lambda f: {'length': f.max_length}}
except AttributeError:
    pass

try:
    # 1.10 or later supports
    types[models.BigAutoField] = {'type': 'bigint'}
except AttributeError:
    pass


def analyze_field(field):
    info = {}
    field_type = type(field)

    if field_type is M2MField:
        info['secondary'] = analyze_model(field.rel.through)
        info['related_name'] = field.rel.related_name
        return info

    if field_type is models.ForeignKey or field_type is models.OneToOneField:
        field_type = type(field.target_field)
        info['related_to'] = '{table}.{field}'.format(
            table=field.related_model._meta.db_table,
            field=field.related_model._meta.pk.attname,
        )

    info['primary_key'] = field.primary_key
    info['unique'] = field.unique
    info['nullable'] = field.null
    info['default'] = field.default

    info.update(types[field_type])
    info.update(info.pop('callback', lambda x: {})(field))

    return info


def analyze_model(model, callback=analyze_field):
    info = {'name': model._meta.db_table, 'fields': OrderedDict()}
    for field in model._meta.fields:
        info['fields'][field.attname] = callback(field)

    for name, field in get_m2m_fields(model).items():
        info['fields'][name] = callback(field)

    return info


def analyze_models(module, condition=lambda model: True, callback=analyze_model):
    models = {}
    for name, model in [(name, getattr(module, name)) for name in dir(module)]:
        if isinstance(model, ModelBase) and condition(model):
            models[name] = callback(model)
    return models

