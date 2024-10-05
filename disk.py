from os import listdir
from os.path import isdir, realpath, normpath
from typing import List


def tree(directory: str) -> List[str]:
    """Search for files in a directory"""
    if not isdir(directory): raise FileNotFoundError
    
    directory = realpath(directory)
    files = []

    for file in listdir(directory):
        path = f"{directory}/{file}"

        if path.endswith("__pycache__"): pass
        elif isdir(path): files += tree(path)
        else: files.append(normpath(path))

    return files
