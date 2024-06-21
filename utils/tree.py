from os import listdir
from os.path import isdir, realpath, normpath


def tree(directory: str) -> list:
    directory = realpath(directory)
    files = []

    for file in listdir(directory):
        path = f"{directory}/{file}"

        if path.endswith("__pycache__"): pass

        elif isdir(path):
            files += tree(path)

        else:
            files.append(normpath(path))

    return files
