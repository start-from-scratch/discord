from logging import getLogger, FileHandler, Formatter, INFO, DEBUG
from rich.logging import RichHandler
from os import system
from os.path import dirname

dir = dirname(__file__)
system(f"{dir}/reset.sh")

logger = getLogger()
logger.setLevel(DEBUG)

handler = FileHandler(
    filename = f"{dir}/latest.log",
    mode = "a",
    encoding = "utf-8"
)
handler.setFormatter(Formatter("%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"))
handler.setLevel(DEBUG)
logger.addHandler(handler)

handler = RichHandler()
handler.setFormatter(Formatter("%(message)s"))
handler.setLevel(INFO)
logger.addHandler(handler)