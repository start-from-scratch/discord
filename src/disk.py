from os import listdir
from os.path import dirname, isdir

def tree(directory: str = dirname(__file__)) -> list:
    files = []

    for file in listdir(directory):
        path = f"{directory}/{file}"

        if path.endswith("__pycache__"): pass

        elif isdir(path):
            files += tree(path)

        else:
            files.append(path)
    
    return files