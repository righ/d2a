# coding: utf-8
from collections import OrderedDict

from django.db.models.base import ModelBase
# The following fields are supported django 1.4 or later.
from django.db.models import (
    AutoField,
    IntegerField, PositiveIntegerField,
    SmallIntegerField, PositiveSmallIntegerField, BigIntegerField,
    DecimalField, FloatField,
    CharField, TextField,
    DateTimeField, DateField, TimeField,
    BooleanField, NullBooleanField,
    ForeignKey, OneToOneField,

    SlugField, URLField, EmailField,
    FileField, FilePathField, ImageField,
    GenericIPAddressField,
)

types = {
    AutoField: {'type': 'int'},
    IntegerField: {'type': 'int'},
    PositiveIntegerField: {'type': 'int'},
    SmallIntegerField: {'type': 'int'},
    PositiveSmallIntegerField: {'type': 'int', 'unsigned': True},
    BigIntegerField: {'type': 'bigint'},
    DecimalField: {'type': 'decimal',
                   'callback': lambda f: {'precision': f.max_digits, 'scale': f.decimal_places}},
    FloatField: {'type': 'float'},
    CharField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    SlugField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    URLField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    EmailField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    FileField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    FilePathField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    ImageField: {'type': 'varchar', 'callback': lambda f: {'length': f.max_length}},
    GenericIPAddressField: {'type': {'postgres': 'inet', 'default': 'char'},
                            'length': 39},

    TextField: {'type': 'text'},
    DateTimeField: {'type': 'datetime'},
    DateField: {'type': 'date'},
    TimeField: {'type': 'time'},
    BooleanField: {'type': 'boolean'},
    NullBooleanField: {'type': 'boolean'},
    ForeignKey: {},
    OneToOneField: {},
}

try:
    # deprecated
    from django.db.models import CommaSeparatedIntegerField
    types[CommaSeparatedIntegerField] = {'type': 'varchar',
                                         'callback': lambda f: {'length': f.max_length}}
except ImportError:
    pass

try:
    # 1.6 or later supports
    from django.db.models import BinaryField
    types[BinaryField] = {'postgres': 'bytea', 'default': 'binary'}
except ImportError:
    pass

try:
    # 1.8 or later supports
    from django.db.models import DurationField
    types[DurationField] = {'type': {'postgres': 'interval', 'default': 'bigint'}}
except ImportError:
    pass

try:
    # 1.8 or later supports
    from django.db.models import UUIDField
    types[UUIDField] = {'type': {'postgres': 'uuid', 'default': 'char'}, 'length': 32}
except ImportError:
    pass

try:
    # 1.10 or later supports
    from django.db.models import BigAutoField
    types[BigAutoField] = {'type': 'bigint'}
except ImportError:
    pass


def analyze_field(field):
    info = {}
    field_type = type(field)

    if field_type is ForeignKey or field_type is OneToOneField:
        field_type = type(field.target_field)
        info['related_to'] = '{table}.{field}'.format(
            table=field.related_model._meta.db_table,
            field=field.related_model._meta.pk.attname,
        )

    info['primary_key'] = field.primary_key
    info['unique'] = field.unique
    info['nullable'] = field.null

    info.update(types[field_type])
    info.update(info.pop('callback', lambda x: {})(field))

    return info


def analyze_model(model, callback=analyze_field):
    info = {'name': model._meta.db_table, 'fields': OrderedDict()}
    for field in model._meta.fields:
        info['fields'][field.attname] = callback(field)

    return info


def analyze_models(module, condition=lambda model: True, callback=analyze_model):
    models = {}
    for name, model in [(name, getattr(module, name)) for name in dir(module)]:
        if isinstance(model, ModelBase) and condition(model):
            models[name] = callback(model)
    return models
