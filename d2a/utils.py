# coding: utf-8
import re


def get_camelcase(s, capitalize=False):
    rs = list(re.finditer(r'(?<=_)\w', s))
    for r in reversed(rs):
        s = s[:r.start()-1] + r.group(0).upper() + s[r.end():]
    return s[0:1].capitalize() + s[1:] if capitalize else s
