# coding: utf-8

from django.db.models.fields.related_descriptors import ManyToManyDescriptor as M2MField

try:
    basestring
    basestring = basestring
except NameError:
    basestring = (str,)
