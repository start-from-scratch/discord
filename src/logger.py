from logging import getLogger, FileHandler, Formatter, INFO
from rich.logging import RichHandler

f_handler = FileHandler(
    filename = "discord.log",
    encoding = "utf-8",
    mode = "a"
)
f_handler.setFormatter(Formatter("%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s"))

r_handler = RichHandler()
r_handler.setFormatter(Formatter("%(message)s"))

logger = getLogger()
logger.setLevel(INFO)
logger.addHandler(f_handler)
logger.addHandler(r_handler)