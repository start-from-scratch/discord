from os.path import isfile, dirname, isdir
from os import mkdir
from atexit import register
from time import time
from zipfile import ZipFile
from logging import getLogger, FileHandler, Formatter, DEBUG
from rich.logging import RichHandler


dir = dirname(dirname(__file__)) + "/logs"


def reset() -> None:
    if not isdir(dir):
        mkdir(dir)

    with open(f"{dir}/latest.log", "w") as f:
        f.write(f"{time()}\n")


logger = getLogger()
logger.setLevel(DEBUG)

reset()

fileHandler = FileHandler(
    filename = f"{dir}/latest.log",
    mode = "a",
    encoding = "utf-8"
)
fileHandler.setFormatter(Formatter("%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"))
logger.addHandler(fileHandler)

richHandler = RichHandler()
richHandler.setFormatter(Formatter("%(message)s"))
logger.addHandler(richHandler)


def compress() -> None:
    if not isfile(f"{dir}/latest.log"):
        return

    with open(f"{dir}/latest.log", "r") as f:
        timestamp = f.readline()[:-2]

    with ZipFile(f"{dir}/archive.zip", "a") as archive:
        archive.write(f"{dir}/latest.log", f"{timestamp}.log")

    fileHandler.close()


register(compress)