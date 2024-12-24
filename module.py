from importlib.util import spec_from_file_location, module_from_spec
from types import ModuleType
from os.path import dirname, realpath, splitext
from typing import Tuple, List, Dict
from sys import modules as loaded_modules

from file import tree as file_tree
import __main__


def parse(path: str) -> Tuple[str]:
    """Gives the module name and real path"""
    root = dirname(realpath(__main__.__file__))
    location = realpath(path)
    name = splitext(location[len(root) + 1:][:-3])[0].replace("/", ".")

    return name, location


def load(path: str) -> Dict[str, ModuleType]:
    """Import a script from a path"""
    location = parse(path)

    if location[0] in loaded_modules: raise ImportError("Module already loaded")

    spec = spec_from_file_location(*location)
    obj = module_from_spec(spec)
    spec.loader.exec_module(obj)

    loaded_modules[location[0]] = obj

    return {location[0]: obj}


def load_directory(directory: str) -> Dict[str, ModuleType]:
    """Import all the scripts of a directory"""
    scripts = list(filter(lambda file: splitext(file)[-1].startswith(".py"), file_tree(directory)))
    modules = {}; 
    
    for script in scripts:
        try:
            obj = load(script)
            modules.update(obj)
        except ImportError:
            pass

    return modules


def unload(modules: Dict[str, ModuleType]) -> None:
    """Unload modules"""
    for name, obj in modules.items():
        del obj
        loaded_modules.pop(name)
