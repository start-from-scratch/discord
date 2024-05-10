from os import listdir, PathLike
from os.path import isdir
from rich.console import Console

console = Console()
status = console.status("")

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