from discord.ext import commands
from discord import application_command, SlashCommandGroup, Embed
from disk import tree, rm
from os.path import dirname, isdir
from os import replace
from logging import getLogger
from pygit2 import clone_repository
from json import load as json_load
from datetime import datetime
from time import time
import __main__

f = open("config.json")
config = json_load(f)
f.close()

logger = getLogger()

class Extender(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.extensions = []
        rm("temp")
        self.load()

    def unload(self) -> None:
        for extension in self.extensions:
            self.bot.unload_extension(extension)
            logger.info(f'Unloaded "{extension}".')

        self.extensions = []

    def load(self) -> None:
        scripts = tree(dirname(__main__.__file__) + "/extensions")

        for script in scripts:
            if script.endswith(".py"):
                self.extensions.append(script[len(dirname(__main__.__file__)) + 1:][:-3].replace("/", "."))
                
                self.bot.load_extension(self.extensions[-1])
                logger.info(f'Loaded "{self.extensions[-1]}".')

    extensions = SlashCommandGroup("extensions")
    
    @extensions.command(
        name = "reload",
        description = "reload all extensions"
    )
    @commands.is_owner()
    async def extensions_reload(self, ctx) -> None:
        embed = Embed(timestamp = datetime.now(), title = "Extensions reload")
        old_extensions = "`, `".join(self.extensions)

        self.unload()

        if config.get("repository"):
            embed.description = f'Got extensions from [this repository]({config.get("repository") or "#"})'

            if len(config["repository"]) >= 1:
                directory = f"temp/{time()}"

                clone_repository(config["repository"], directory)
                rm(dirname(__file__) + "/extensions")
                replace(f"{directory}/src/extensions", dirname(__file__) + "/extensions")

        self.load()
        extensions = "`, `".join(self.extensions)

        embed.add_field(name = ":heavy_minus_sign: unloaded", value = old_extensions)
        embed.add_field(name = ":heavy_plus_sign: loaded", value = extensions)
        
        await ctx.respond(embed = embed)

    @extensions.command(
        name = "list",
        description = "get the list of loaded extensions"
    )
    @commands.is_owner()
    async def extensions_list(self, ctx) -> None:
        embed = Embed(timestamp = datetime.now(), title = "Extensions", description = "`, `".join(self.extensions))
        await ctx.respond(embed = embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Extender(bot))
