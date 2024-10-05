from inspect import getfullargspec


class Cogs(dict):
    def __init__(self) -> None:
        super().__init__()
        self.kwargs = {}

    def add_cog(self, obj: object) -> None:
        if obj.__name__ in self: return
        
        spec = getfullargspec(obj)

        requirements = spec.args + spec.kwonlyargs
        kwargs = {}
        [kwargs.__setitem__(key, value) for key, value in self.kwargs.items() if key in requirements]

        super().__setitem__(obj.__name__, obj(**kwargs))

    def remove_cog(self, name: str) -> None:
        obj = super().__getitem__(name)

        del obj
        super().pop(name)

    def cog(self, obj: object) -> object:
        self.add_cog(obj)
        return obj


class CogsGroups(dict):
    def __init__(self) -> None:
        super().__init__()
    
    def __setitem__(self, name: str, kwargs: dict) -> None:
        obj = super().get(name) or Cogs()
        obj.kwargs = kwargs

        super().__setitem__(name, obj)
    

cogs_groups = CogsGroups()


def get_cogs(name: str = None) -> Cogs:
    if name == None: name = "default"
    if name not in cogs_groups: cogs_groups[name] = {}

    obj = cogs_groups.get(name)
    
    return obj
