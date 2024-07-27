import importlib
from types import ModuleType

from utils import get_main_dir


def get_module_path(file_path: str) -> str:
    root: str = get_main_dir()
    path: str = file_path[len(root) + 1:][:-3] \
        .replace("\\", ".") \
        .replace("/", ".")

    return path


def load(file_path: str) -> ModuleType:
    name: str = get_module_path(file_path)

    spec = importlib.util.spec_from_file_location(name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return module


def unload(module: ModuleType) -> None:
    del module