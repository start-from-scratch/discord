from inspect import getfullargspec
from typing import Union, Type
from types import FunctionType


cogs = {"callables": {}, "kwargs": {}}


def add_cog(callable: Union[Type, FunctionType]) -> None:
    if callable.__name__ in cogs["callables"]: 
        raise NameError(f"A callable object with the same name ({callable.__name__}) has already been loaded")
            
    spec = getfullargspec(callable)
    requirements = spec.args + spec.kwonlyargs
    
    kwargs = {}
    for key, value in cogs["kwargs"].items():
        if key not in requirements:
            continue
        
        kwargs[key] = value

    cogs["callables"][callable.__name__] = callable(**kwargs)

def cog(callable: Union[Type, FunctionType]) -> object:
    try:
        add_cog(callable)
    except NameError:
        pass
    
    return callable
