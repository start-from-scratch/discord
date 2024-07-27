from discord.ext import commands
from logging import getLogger
from os.path import dirname, normpath, realpath, join, basename

from utils import tree, clone
import __main__


class Loader:
    def __init__(self, bot: commands.Bot, directory: str, repository: str | None = None) -> None:
        self.bot: commands.Bot = bot
        self.directory: str = directory
        self.repository: str | None = repository

        self.logger = getLogger()
        self.root: str = dirname(realpath(__main__.__file__))
        self.cogs: list[str] = []

    def load(self) -> list[str]:
        files: list[str] = tree(join(self.root, self.directory))
        modules: list[str] = []

        for file in files:
            if file.endswith(".py"):
                modules.append(file[len(self.root) + 1:][:-3].replace("\\", ".").replace("/", "."))

        for module in modules:
            self.bot.load_extension(module)
            self.logger.info('Loaded "%s".' % module)

        self.modules = modules
        return self.modules

    def unload(self) -> None:
        for extension in self.modules:
            self.bot.unload_extension(extension)
            self.logger.info(f'Unloaded "{extension}".')

        self.modules = []
    
    def pull(self) -> list[str]:
        if not self.repository:
            return self.modules
        
        self.unload()
        tmpdir: str = clone(self.repository)
        
        for source in tree(join(str(tmpdir), self.directory)):
            path: str = source[len(join(tmpdir, self.directory)) + 1:]
            destination: str = join(self.root, self.directory, path)

            with open(source, "r") as f:
                content: str = f.read()

            with open(destination, "w") as f:
                f.write(content)

        return self.load()
