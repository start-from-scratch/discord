from os.path import isdir
from os import mkdir

def create_path(path: str) -> None:
    directories: list[str] = path.replace("\\", "/").split("/")

    for index in range(len(directories)):
        path = "/".join(directories[:index + 1])

        if not isdir(path):
            mkdir(path)