import importlib
from types import ModuleType

from .disk import get_main_dir, tree


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


def find(directory: str) -> list[str]:
    files: list[str] = tree(directory)
    modules: list[str] = []

    [modules.append(file) if file.endswith(".py") else None for file in files]

    return modules
