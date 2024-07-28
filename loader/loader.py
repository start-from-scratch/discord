from discord.ext import commands
from logging import getLogger
from os.path import join
from types import ModuleType
from tempfile import mkdtemp

from .git import clone
from .disk import get_main_dir
from .modules import load, unload, tree
from .cogs import has_cog
import __main__


class Loader:
    def __init__(self, bot: commands.Bot, directory: str, repository: str | None = None, **kwargs) -> None:
        self.bot: commands.Bot = bot
        self.directory: str = directory
        self.repository: str | None = repository
        self.kwargs: dict = kwargs

        self.logger = getLogger()
        self.root: str = get_main_dir()

        self.modules: list[ModuleType] = {}
        self.cogs: list[str] = []

    def load(self) -> list[str]:
        files: list[str] = tree(self.directory)
        modules: list[ModuleType] = []
        index: int = len(self.bot.cogs.keys())

        for file in files:
            module: ModuleType = load(file)

            if has_cog(module):
                module.setup(self.bot, **self.kwargs)
                modules.append(module)

                self.logger.info(f'Loaded "%s".' % module.__name__)
            else:
                unload(module)
        
        self.modules, self.cogs = modules, list(self.bot.cogs.keys())[index:]
        return self.cogs

    def unload(self) -> None:
        for cog in self.cogs:
            self.bot.remove_cog(cog)

        for module in self.modules:
            unload(module)

            self.logger.info('Unloaded "%s".' % module.__name__)

        self.modules = []
        self.cogs = []
    
    def update(self) -> list[str]:
        if not self.repository:
            return self.cogs
        
        tmpdir: str = mkdtemp()

        self.unload()
        clone(self.repository, tmpdir)
        
        for source in tree(join(str(tmpdir), self.directory)):
            path: str = source[len(join(tmpdir, self.directory)) + 1:]
            destination: str = join(self.root, self.directory, path)

            with open(source, "r") as f:
                content: str = f.read()

            with open(destination, "w") as f:
                f.write(content)

        return self.load()
