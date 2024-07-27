from discord.ext import commands
from discord import SlashCommandGroup, Embed, ApplicationContext
from os.path import dirname, realpath, normpath, basename, exists
from os import remove
from shutil import move
from logging import getLogger
from datetime import datetime

from utils.disk import tree
from utils.git import clone
import __main__


root = dirname(realpath(__main__.__file__))
logger = getLogger()
    

class Loader(commands.Cog):
    def __init__(self, bot: commands.Bot, config: dict) -> None:
        self.bot: commands.Bot = bot
        self.modules: list[str] = []
        self.config: dict = config
    
        self.load()
        
    group = SlashCommandGroup("modules")

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
    
    @group.command(
        name = "reload",
        description = "reload all modules"
    )
    @commands.is_owner()
    async def modules_reload(self, ctx: ApplicationContext) -> None:
        embed = Embed(timestamp = datetime.now(), title = "modules reload")
        old_modules = "`, `".join(self.modules)

        self.unload()

        tmpdir = clone(self.config["repository"]["url"])
        remove(tmpdir + self.config["repository"]["cogs"] + f"/{basename(__file__)}")

        for module in tree(tmpdir + self.config["repository"]["cogs"]):
            if not module == realpath(dirname(__file__)):
                if exists(f"{root}/{self.config["repository"]["cogs"]}/{basename(module)}"):
                    remove(f"{root}/{self.config["repository"]["cogs"]}/{basename(module)}")
                    
                move(module, f"{root}/{self.config["repository"]["cogs"]}")

        self.load()
        modules = "`, `".join(self.modules)

        embed.add_field(name = ":heavy_minus_sign: unloaded", value = old_modules)
        embed.add_field(name = ":heavy_plus_sign: loaded", value = modules)
        
        await ctx.respond(embed = embed)

    @group.command(
        name = "list",
        description = "get the list of loaded modules"
    )
    @commands.is_owner()
    async def modules_list(self, ctx) -> None:
        description = "`, `".join(self.modules) if len(self.modules) > 1 else f"`{self.modules[0]}`"
        embed = Embed(timestamp = datetime.now(), title = "modules", description = description)
        await ctx.respond(embed = embed)
