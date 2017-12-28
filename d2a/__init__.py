from .django import analyze_models, analyze_model
from .alchemy import declare as alchemy_declare


def transfer(models, exports, db=None, model_condition=lambda x: x):
    for name, alchemy_info in analyze_models(models, condition=model_condition).items():
        exports[name] = alchemy_declare(alchemy_info, db)


def copy(model, db=None):
    alchemy_info = analyze_model(model)
    return alchemy_declare(alchemy_info, db)
