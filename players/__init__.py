import importlib
import pkgutil

# Dynamically import all modules in the players directory
__all__ = []
for _, module_name, _ in pkgutil.iter_modules(__path__):
    module = importlib.import_module(f".{module_name}", __package__)
    for class_name, class_obj in module.__dict__.items():
        if isinstance(class_obj, type):  # Check if it's a class
            globals()[class_name] = class_obj
            __all__.append(class_name)