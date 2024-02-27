from logging import getLogger, FileHandler, Formatter, DEBUG
from rich.logging import RichHandler

r_handler = RichHandler()
r_handler.setFormatter(Formatter("%(message)s"))

logger = getLogger()
logger.setLevel(DEBUG)
logger.addHandler(r_handler)