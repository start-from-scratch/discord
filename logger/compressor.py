from zipfile import ZipFile
from os.path import isfile


def create_empty(path: str) -> None:
    if isfile(path): return

    archive = ZipFile(path, "w")
    archive.close()


def move(file: str, archive: str, alias: str | None = None) -> None:
    archive: ZipFile = ZipFile(archive, "a")
    archive.write(file, alias)
    archive.close()