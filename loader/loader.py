from discord.ext import commands
from logging import getLogger
from os.path import join
from types import ModuleType

from utils import tree, clone, get_main_dir
from .modules import get_module_path, load, unload
import __main__


class Loader:
    def __init__(self, bot: commands.Bot, directory: str, repository: str | None = None, **kwargs) -> None:
        self.bot: commands.Bot = bot
        self.directory: str = directory
        self.repository: str | None = repository
        self.kwargs: dict = kwargs

        self.logger = getLogger()
        self.root: str = get_main_dir()

        self.modules: dict[str: ModuleType] = {}
        self.cogs: list[str] = []

    def load(self) -> list[str]:
        modules: dict[str: ModuleType] = {}
        start_cog: int = len(self.bot.cogs.keys())

        for file in tree(join(self.root, self.directory)):
            if file.endswith(".py"):
                cog: ModuleType = load(file)
                cog.setup(self.bot, **self.kwargs)

                modules[get_module_path(file)] = cog
                self.logger.info(f'Loaded "%s".' % list(modules.keys())[-1])
        
        self.modules, self.cogs = modules, list(self.bot.cogs.keys())[start_cog:]
        return self.cogs

    def unload(self) -> None:
        for cog in self.cogs:
            self.bot.remove_cog(cog)

        for module in list(self.modules.keys()):
            unload(self.modules[module])

            self.logger.info('Unloaded "%s".' % module)

        self.modules = []
        self.cogs = []
    
    def update(self) -> list[str]:
        if not self.repository:
            return self.cogs
        
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
