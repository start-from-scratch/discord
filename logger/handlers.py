from logging import FileHandler, Formatter
from rich.logging import RichHandler
from os.path import join


def file(directory: str, level: int) -> FileHandler:
    fileHandler: FileHandler = FileHandler(
        filename = join(directory, "latest.log"),
        mode = "w",
        encoding = "utf-8"
    )

    fileHandler.setFormatter(Formatter("%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"))
    fileHandler.setLevel(level)

    return fileHandler


def rich(level: int) -> RichHandler:
    richHandler: RichHandler = RichHandler()

    richHandler.setFormatter(Formatter("%(message)s"))
    richHandler.setLevel(level)

    return richHandler
