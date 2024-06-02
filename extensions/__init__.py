from discord.ext import commands
from discord import SlashCommandGroup, Embed
from os.path import dirname
from os import system
from logging import getLogger
from json import load as json_load
from datetime import datetime

import __main__

f = open("config.json")
config = json_load(f)
f.close()

logger = getLogger()

class Extender(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        system(f"{dirname(__file__)}/list.sh {dirname(__main__.__file__)}")
        with open(f"{dirname(__file__)}/scripts/list.txt", "r") as f:
            self.extensions = f.read().split("\n")[:-1]
        
        self.load()

    def unload(self) -> None:
        for extension in self.extensions:
            self.bot.unload_extension(extension)
            logger.info(f'Unloaded "{extension}".')

        self.extensions = []

    def load(self) -> None:
        for script in self.extensions:
            self.bot.load_extension(script)
            logger.info(f'Loaded "{script}".')

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

        system(f"{dirname(__file__)}/update.sh {dirname(__main__.__file__)}/config.json")
        with open(f"{dirname(__file__)}/scripts/list.txt", "r") as f:
            self.extensions = f.read().split("\n")[:-1]

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
        description = "`, `".join(self.extensions) if len(self.extensions) > 1 else f"`{self.extensions[0]}`"
        embed = Embed(timestamp = datetime.now(), title = "Extensions", description = description)
        await ctx.respond(embed = embed)

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Extender(bot))
