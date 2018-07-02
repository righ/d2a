# coding: utf-8
from django.db import models
from django.contrib.postgres import fields as postgres_fields

from sqlalchemy import types as default_types
from sqlalchemy.dialects import postgresql as postgresql_types
from sqlalchemy.dialects import mysql as mysql_types

from .compat import M2MField


mapping = {
    models.AutoField: {
        '_default_type': default_types.INT,
        '_postgresql_type': postgresql_types.INTEGER,
        '_mysql_type': mysql_types.INTEGER,
        'autoincrement': True,
    },
    models.IntegerField: {
        '_default_type': default_types.INT,
        '_postgresql_type': postgresql_types.INTEGER,
        '_mysql_type': mysql_types.INTEGER,
    },
    models.PositiveIntegerField: {
        '_default_type': default_types.INT, 
        '_postgresql_type': postgresql_types.INTEGER,
        '_mysql_type': mysql_types.INTEGER,
        '_mysql_type_option': {'unsigned': True},
    },
    models.SmallIntegerField: {
        '_default_type': default_types.SMALLINT, 
        '_postgresql_type': postgresql_types.SMALLINT,
        '_mysql_type': mysql_types.SMALLINT,
    },
    models.PositiveSmallIntegerField: {
        '_default_type': default_types.SMALLINT, 
        '_postgresql_type': postgresql_types.SMALLINT, 
        '_mysql_type': mysql_types.SMALLINT, 
        '_mysql_type_option': {'unsigned': True},
    },
    models.BigIntegerField: {
        '_default_type': default_types.BIGINT, 
        '_postgresql_type': postgresql_types.BIGINT,
        '_mysql_type': mysql_types.BIGINT,
    },
    models.DecimalField: {
        '_default_type': default_types.DECIMAL,
        '_postgresql_type': postgresql_types.NUMERIC,
        '_mysql_type': mysql_types.NUMERIC,
        '_callback': lambda f: {
            '_default_type_option': {'precision': f.max_digits, 'scale': f.decimal_places},
            '_postgresql_type_option': {'precision': f.max_digits, 'scale': f.decimal_places},
            '_mysql_type_option': {'precision': f.max_digits, 'scale': f.decimal_places},
        }
    },
    models.FloatField: {
        '_default_type': default_types.FLOAT,
        '_postgresql_type': postgresql_types.FLOAT,
        '_mysql_type': mysql_types.FLOAT,
    },
    models.CharField: {
        '_default_type': default_types.VARCHAR, 
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
        },
    },
    models.SlugField: {
        '_default_type': default_types.VARCHAR, 
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
        },
    },
    models.URLField: {
        '_default_type': default_types.VARCHAR, 
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
        },
    },
    models.EmailField: {
        '_default_type': default_types.VARCHAR, 
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
        },
    },
    models.FileField: {
        '_default_type': default_types.VARCHAR, 
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
        },
    },
    models.FilePathField: {
        '_default_type': default_types.VARCHAR, 
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
        },
    },
    models.ImageField: {
        '_default_type': default_types.VARCHAR, 
        '_callback': lambda f: {
            '_default_type_option': {'length': f.max_length},
        },
    },
    models.GenericIPAddressField: {
        '_default_type': default_types.CHAR,
        '_postgresql_type': postgresql_types.INET, 
        '_default_type_option': {'length': 39},
    },
    models.BinaryField: {
        '_default_type': default_types.Binary,
        '_postgresql_type': postgresql_types.BYTEA,
        '_mysql_type': mysql_types.LONGBLOB,
    },
    models.DurationField: {
        '_default_type': default_types.BIGINT,
        '_postgresql_type': postgresql_types.INTERVAL,
    },
    models.UUIDField: {
        '_default_type': default_types.CHAR,
        '_postgresql_type': postgresql_types.UUID,
        '_default_type_option': {'length': 32},
    },
    models.TextField: {
        '_default_type': default_types.Text,
    },
    models.DateTimeField: {
        '_default_type': default_types.DateTime,
    },
    models.DateField: {
        '_default_type': default_types.Date,
    },
    models.TimeField: {
        '_default_type': default_types.Time,
    },
    models.BooleanField: {
        '_default_type': default_types.Boolean,
    },
    models.NullBooleanField: {
        '_default_type': default_types.Boolean,
        'null': True,
    },
    models.ForeignKey: {
        '_callback': lambda f: {
            '_callback': lambda f: (mapping[type(f.target_field)], f.target_field),
            '_rel_option': {
                '_logical_name': f.name, 
                '_back': f.related_query_name(),
                '_target': f.related_model()._meta.db_table,
            }, 
            '_fk_option': {
                'column': '{meta.db_table}.{meta.pk.attname}'.format(meta=f.related_model._meta),
                'ondelete': f.remote_field.on_delete.__name__,
            },
        },
    },
    models.OneToOneField: {
        '_callback': lambda f: {
            '_callback': lambda f: (mapping[type(f.target_field)], f.target_field),
            '_rel_option': {
                '_logical_name': f.name, 
                '_back': f.related_query_name(), 
                '_target': f.related_model()._meta.db_table,
                'uselist': False,
            }, 
            '_fk_option': {
                'column': '{meta.db_table}.{meta.pk.attname}'.format(meta=f.related_model._meta),
                'ondelete': f.remote_field.on_delete.__name__,
            },
        },
    },
    M2MField: {
        '_callback': lambda f: {
            '_rel_option': {
                '_secondary_model': f.rel.through, 
                '_target_field': f.field.m2m_target_field_name(),
                '_remote_primary_field': f.field.m2m_column_name(),
                '_remote_secondary_field': f.field.m2m_reverse_name(),
                '_back': f.field.related_query_name(),
                '_target': f.rel.model._meta.db_table,
            },
        } if not f.reverse else {}
    },
}

try:
    # deprecated
    mapping[models.CommaSeparatedIntegerField] = {
        '_default_type': default_types.VARCHAR,
        '_callback': lambda f: {'_default_type_option': {'length': f.max_length}}
    }
except AttributeError:
    pass

try:
    # 1.10 or later supports
    mapping[models.BigAutoField] = {
        '_default_type': default_types.BIGINT, 
        '_postgresql_type': postgresql_types.BIGINT,
        '_mysql_type': mysql_types.BIGINT,
        'autoincrement': True,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.ArrayField] = {
        '_default_type': default_types.ARRAY,
        '_postgresql_type': postgresql_types.ARRAY,
        '_callback': lambda f: {
            '_default_type_option': {'item_type': mapping[type(f.base_field)]['_default_type']},
            '_postgresql_type_option': {'item_type': mapping[type(f.base_field)]['_default_type']},
        }
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.JSONField] = {
        '_default_type': default_types.JSON,
        '_postgresql_type': postgresql_types.JSON,
    }
except AttributeError:
    pass


def alias(new_field, existing_field):
    mapping[new_field] = mapping[existing_field]

