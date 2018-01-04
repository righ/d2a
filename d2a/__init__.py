# coding: utf-8
import re

from .django import analyze_models, analyze_model
from .alchemy import declare, existing


def get_camelcase(s):
    rs = list(re.finditer(r'(?<=_)\w', s))
    for r in reversed(rs):
        s = s[:r.start()-1] + r.group(0).upper() + s[r.end():]
    return s


def transfer(models, exports, db=None, back_type=None, model_condition=lambda x: x, name_formatter=get_camelcase):
    for model in analyze_models(models, condition=model_condition).values():
        declare(model, db=db, back_type=back_type)

    for django_model, alchemy_model in existing.items():
        if models.__name__ == django_model.__module__:
            exports[name_formatter(django_model._meta.object_name)] = alchemy_model

