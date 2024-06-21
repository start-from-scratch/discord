from discord.ext import commands
from discord import SlashCommandGroup, Embed, Option
from os.path import dirname, realpath, normpath
from shutil import move
from tempfile import mkdtemp
from logging import getLogger
from json import load as load_json
from datetime import datetime
from pygit2 import clone_repository

from utils.tree import tree
import __main__


root = dirname(realpath(__main__.__file__))
logger = getLogger()

with open(f"{root}/config.json", "r") as f:
    config = load_json(f)
    

class Loader(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.modules = []
    
        self.load()

    def unload(self) -> None:
        for extension in self.modules:
            self.bot.unload_extension(extension)
            logger.info(f'Unloaded "{extension}".')

        self.modules = []

    def load(self) -> None:
        files = tree(dirname(__file__))
        modules = []

        for file in files:
            if not any([
                not file.endswith(".py"),
                file == normpath(realpath(__file__))
            ]):
                modules.append(file[len(root) + 1:][:-3].replace("\\", ".").replace("/", "."))

        for module in modules:
            self.bot.load_extension(module)
            logger.info('Loaded "%s".', module)

        self.modules = modules

    modules = SlashCommandGroup("modules")
    
    @modules.command(
        name = "reload",
        description = "reload all modules"
    )
    @commands.is_owner()
    async def modules_reload(self, ctx) -> None:
        embed = Embed(timestamp = datetime.now(), title = "modules reload")
        old_modules = "`, `".join(self.modules)

        self.unload()

        tmpdir = mkdtemp()
        repo = clone_repository(config["repository"]["url"], tmpdir)
        print(tree(tmpdir))
        for module in tree(tmpdir + config["repository"]["cogs"]):
            print(module, realpath(dirname(__file__)))
            if not module == realpath(dirname(__file__)):
                move(module, dirname(__file__))

        repo.free()

        self.load()
        modules = "`, `".join(self.modules)

        embed.add_field(name = ":heavy_minus_sign: unloaded", value = old_modules)
        embed.add_field(name = ":heavy_plus_sign: loaded", value = modules)
        
        await ctx.respond(embed = embed)

    @modules.command(
        name = "list",
        description = "get the list of loaded modules"
    )
    @commands.is_owner()
    async def modules_list(self, ctx) -> None:
        description = "`, `".join(self.modules) if len(self.modules) > 1 else f"`{self.modules[0]}`"
        embed = Embed(timestamp = datetime.now(), title = "modules", description = description)
        await ctx.respond(embed = embed)


def setup(bot: commands.Bot) -> None:
    bot.add_cog(Loader(bot))
