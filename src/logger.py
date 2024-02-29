from logging import getLogger, FileHandler, Formatter, INFO
from rich.logging import RichHandler
from os import makedirs, rename
from os.path import isdir, isfile
from time import time

directory = f"logs"
file = directory + "/latest.log"

if not isdir(directory): 
    makedirs(directory)

if isfile(file):
    old = open(file, "r", encoding = "utf-8")
    timestamp = old.readline()[:-1]

    old.close()
    rename(file, f"{directory}/{timestamp}.log")

new = open(file, "w")
new.write(f"{time()}\n")
new.close()

logger = getLogger()
logger.setLevel(INFO)

handler = FileHandler(
    filename = file,
    mode = "a",
    encoding = "utf-8"
)
handler.setFormatter(Formatter("%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"))
logger.addHandler(handler)

handler = RichHandler()
handler.setFormatter(Formatter("%(message)s"))
logger.addHandler(handler)