from logging import Logger, DEBUG, getLogger
from atexit import register
from os.path import join
from time import time

from .compressor import create_empty, move
from .handlers import rich, file
from .disk import create_path


def init(directory: str, archive: str = "archive.zip", level: int = DEBUG, file_handler_level: int = DEBUG) -> Logger:
    create_path(directory)
    
    create_empty(join(directory, archive))
    register(move, file=join(directory, "latest.log"), alias=f"{time()}.log", archive=join(directory, archive))

    logger = getLogger()

    logger.setLevel(level)
    
    logger.addHandler(rich(level))
    logger.addHandler(file(directory, file_handler_level))

    return logger