from os import PathLike, chmod, access, W_OK, remove
from os.path import isdir, isfile, exists
from rich.console import Console
from shutil import rmtree
from stat import S_IWUSR

console = Console()
status = console.status("")

def onerror(func, path, exc_info):
    if not access(path, W_OK):
        chmod(path, S_IWUSR)
        func(path)
    else:
        raise

def rm(path: PathLike) -> list:
    if not exists(path):
        return
    
    status.update(f'[bold green]Removing "{path}"...')
    status.start()

    if isdir(path):
        rmtree(path, onerror = onerror)
    elif isfile(path):
        remove(path)

    console.log(f'[green]Removed "{path}".[/green]')
    status.stop()