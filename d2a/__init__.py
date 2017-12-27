from .django import analyze_models
from .alchemy import declare as alchemy_declare


def copy(models, exports, db=None, model_condition=lambda x: x):
    for name, model_info in analyze_models(models, condition=model_condition).items():
        exports[name] = alchemy_declare(model_info, db)
