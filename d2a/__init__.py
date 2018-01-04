# coding: utf-8
import re

from .django import analyze_models, analyze_model
from .alchemy import declare as alchemy_declare, m2m_models

def get_camelcase(s):
    rs = list(re.finditer(r'(?<=_)\w', s))
    for r in reversed(rs):
        s = s[:r.start()-1] + r.group(0).upper() + s[r.end():]
    return s


def transfer(models, exports, db=None, model_condition=lambda x: x, m2m_model_naming=get_camelcase):
    for name, alchemy_info in analyze_models(models, condition=model_condition).items():
        exports[name] = alchemy_declare(alchemy_info, db)
    
    for name, alchemy_model in m2m_tables.items():
        exports[m2m_model_naming(name)] = alchemy_model


def copy(model, db=None):
    alchemy_info = analyze_model(model)
    return alchemy_declare(alchemy_info, db)
