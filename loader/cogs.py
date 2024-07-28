from types import ModuleType


def has_cog(module: ModuleType) -> bool:
    return "setup" in dir(module)
