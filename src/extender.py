from discord.ext import commands
from discord import application_command
from disk import tree
from os.path import dirname, isdir
from os import replace, chmod, W_OK, access
from logging import getLogger
from pygit2 import clone_repository
from json import load as json_load
from shutil import rmtree
from time import time
from stat import S_IWUSR

f = open("config.json")
config = json_load(f)
f.close()

logger = getLogger()

def onerror(func, path, exc_info):
    if not access(path, W_OK):
        chmod(path, S_IWUSR)
        func(path)
    else:
        raise

class Extender(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.directory = dirname(__file__) + "/extensions"
        self.extensions = []
        self.load()

    def unload(self) -> None:
        for extension in self.extensions:
            self.bot.unload_extension(extension)
            logger.info(f'Unloaded "{extension}".')

        self.extensions = []

    def load(self) -> None:
        scripts = tree(self.directory)

        for script in scripts:
            if script.endswith(".py"):
                self.extensions.append(f"extensions.{script[:-3][len(self.directory) + 1:].replace('/', '.')}")
                
                self.bot.load_extension(self.extensions[-1])
                logger.info(f'Loaded "{self.extensions[-1]}".')

    @commands.slash_command(
        name = "reload",
        description = "reload all extensions"
    )
    @commands.is_owner()
    async def reload(self, ctx: application_command()) -> None:
        self.unload()

        if config.get("repository"):
            if isdir("temp"):
                chmod("temp", S_IWUSR)
                rmtree("temp", onerror = onerror)

            if len(config["repository"]) >= 1:
                clone_repository(config["repository"], "temp")
                rmtree(dirname(__file__) + "/extensions", onerror = onerror)
                replace("temp/src/extensions", dirname(__file__) + "/extensions")

        self.load()

        extensions = "`, `".join(self.extensions)
        await ctx.respond(f"Loaded `{extensions}`.")

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Extender(bot))