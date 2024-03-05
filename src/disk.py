from os import listdir, PathLike, chmod, access, W_OK, remove
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

def tree(directory: PathLike) -> list:
    files = []
    directories = []

    status.update(f'[bold green]Listing directory "{directory}"...')
    status.start()

    for file in listdir(directory):
        file = f"{directory}/{file}"
        console.log(f'[green]Found "{file}".[/green]')

        if isdir(file):
            directories.append(file)

        else:
            files.append(file)
    
    status.stop()

    for _directory in directories:
        files += tree(_directory)

    return files