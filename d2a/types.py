# coding: utf-8
from django.db import models
from django.contrib.postgres import fields as postgres_fields

from sqlalchemy import types as default_types
from sqlalchemy.dialects import postgresql as postgresql_types
from sqlalchemy.dialects import mysql as mysql_types

from .compat import M2MField


mapping = {
    models.AutoField: {
        'default_type': default_types.INT,
        'postgresql_type': postgresql_types.INTEGER,
        'mysql_type': mysql_types.INTEGER,
        'autoincrement': True,
    },
    models.IntegerField: {
        'default_type': default_types.INT,
        'postgresql_type': postgresql_types.INTEGER,
        'mysql_type': mysql_types.INTEGER,
    },
    models.PositiveIntegerField: {
        'default_type': default_types.INT, 
        'postgresql_type': postgresql_types.INTEGER,
        'mysql_type': mysql_types.INTEGER,
        'mysql_type_option': {'unsigned': True},
    },
    models.SmallIntegerField: {
        'default_type': default_types.SMALLINT, 
        'postgresql_type': postgresql_types.SMALLINT,
        'mysql_type': mysql_types.SMALLINT,
    },
    models.PositiveSmallIntegerField: {
        'default_type': default_types.SMALLINT, 
        'postgresql_type': postgresql_types.SMALLINT, 
        'mysql_type': mysql_types.SMALLINT, 
        'mysql_type_option': {'unsigned': True},
    },
    models.BigIntegerField: {
        'default_type': default_types.BIGINT, 
        'postgresql_type': postgresql_types.BIGINT,
        'mysql_type': mysql_types.BIGINT,
    },
    models.DecimalField: {
        'default_type': default_types.DECIMAL,
        'postgresql_type': postgresql_types.NUMERIC,
        'mysql_type': mysql_types.NUMERIC,
        'callback': lambda f: {
            'default_type_option': {'precision': f.max_digits, 'scale': f.decimal_places},
            'postgresql_type_option': {'precision': f.max_digits, 'scale': f.decimal_places},
            'mysql_type_option': {'precision': f.max_digits, 'scale': f.decimal_places},
        }
    },
    models.FloatField: {
        'default_type': default_types.FLOAT,
        'default_type': postgresql_types.FLOAT,
        'default_type': mysql_types.FLOAT,
    },
    models.CharField: {
        'default_type': default_types.VARCHAR, 
        'callback': lambda f: {
            'default_type_option': {'length': f.max_length},
        },
    },
    models.SlugField: {
        'default_type': default_types.VARCHAR, 
        'callback': lambda f: {
            'default_type_option': {'length': f.max_length},
        },
    },
    models.URLField: {
        'default_type': default_types.VARCHAR, 
        'callback': lambda f: {
            'default_type_option': {'length': f.max_length},
        },
    },
    models.EmailField: {
        'default_type': default_types.VARCHAR, 
        'callback': lambda f: {
            'default_type_option': {'length': f.max_length},
        },
    },
    models.FileField: {
        'default_type': default_types.VARCHAR, 
        'callback': lambda f: {
            'default_type_option': {'length': f.max_length},
        },
    },
    models.FilePathField: {
        'default_type': default_types.VARCHAR, 
        'callback': lambda f: {
            'default_type_option': {'length': f.max_length},
        },
    },
    models.ImageField: {
        'default_type': default_types.VARCHAR, 
        'callback': lambda f: {
            'default_type_option': {'length': f.max_length},
        },
    },
    models.GenericIPAddressField: {
        'default_type': default_types.CHAR,
        'postgresql_type': postgresql_types.INET, 
        'default_type_option': {'length': 39},
    },
    models.BinaryField: {
        'default_type': default_types.Binary,
        'postgresql_type': postgresql_types.BYTEA,
        'mysql_type': mysql_types.LONGBLOB,
    },
    models.DurationField: {
        'default_type': default_types.BIGINT,
        'postgresql_type': postgresql_types.INTERVAL,
    },
    models.UUIDField: {
        'default_type': default_types.CHAR,
        'postgresql_type': postgresql_types.UUID,
        'default_type_option': {'length': 32},
    },
    models.TextField: {
        'default_type': default_types.Text,
    },
    models.DateTimeField: {
        'default_type': default_types.DateTime,
    },
    models.DateField: {
        'default_type': default_types.Date,
    },
    models.TimeField: {
        'default_type': default_types.Time,
    },
    models.BooleanField: {
        'default_type': default_types.Boolean,
    },
    models.NullBooleanField: {
        'default_type': default_types.Boolean,
        'null': True,
    },
    models.ForeignKey: {
        'callback': lambda f: {
            'callback': lambda f: (mapping[type(f.target_field)], f.target_field),
            'rel_option': {
                'logical_name': f.name, 
                'back': f.related_query_name(),
                'target': f.related_model()._meta.db_table,
            }, 
            'fk_option': {
                'column': '{meta.db_table}.{meta.pk.attname}'.format(meta=f.related_model._meta),
                'ondelete': f.remote_field.on_delete.__name__,
            },
        },
    },
    models.OneToOneField: {
        'callback': lambda f: {
            'callback': lambda f: (mapping[type(f.target_field)], f.target_field),
            'rel_option': {
                'logical_name': f.name, 
                'back': f.related_query_name(), 
                'target': f.related_model()._meta.db_table,
                'uselist': False,
            }, 
            'fk_option': {
                'column': '{meta.db_table}.{meta.pk.attname}'.format(meta=f.related_model._meta),
                'ondelete': f.remote_field.on_delete.__name__,
            },
        },
    },
    M2MField: {
        'callback': lambda f: {
            'rel_option': {
                'secondary_model': f.rel.through, 
                'target_field': f.field.m2m_target_field_name(),
                'remote_primary_field': f.field.m2m_column_name(),
                'remote_secondary_field': f.field.m2m_reverse_name(),
                'back': f.field.related_query_name(),
                'target': f.rel.model._meta.db_table,
            },
        } if not f.reverse else {}
    },
}

try:
    # deprecated
    mapping[models.CommaSeparatedIntegerField] = {
        'default_type': default_types.VARCHAR,
        'callback': lambda f: {'default_type_option': {'length': f.max_length}}
    }
except AttributeError:
    pass

try:
    # 1.10 or later supports
    mapping[models.BigAutoField] = {
        'default_type': default_types.BIGINT, 
        'postgresql_type': postgresql_types.BIGINT,
        'mysql_type': mysql_types.BIGINT,
        'autoincrement': True,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.ArrayField] = {
        'default_type': default_types.ARRAY,
        'postgresql_type': postgresql_types.ARRAY,
    }
except AttributeError:
    pass

try:
    mapping[postgres_fields.JSONField] = {
        'default_type': default_types.JSON,
        'postgresql_type': postgresql_types.JSON,
    }
except AttributeError:
    pass


def alias(new_field, existing_field):
    mapping[new_field] = mapping[existing_field]

