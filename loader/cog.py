from discord.ext import commands
from discord import SlashCommandGroup, Embed, ApplicationContext
from datetime import datetime

from .loader import Loader
    

class LoaderCog(commands.Cog):
    def __init__(self, bot: commands.Bot, directory: str, repository: str | None = None) -> None:
        self.bot: commands.Bot = bot

        self.loader: Loader = Loader(bot, directory, repository)
        self.loader.load()
        
    group = SlashCommandGroup("modules")

    @group.command(
        name = "reload",
        description = "reload all modules"
    )
    @commands.is_owner()
    async def modules_reload(self, ctx: ApplicationContext) -> None:
        embed = Embed(timestamp = datetime.now(), title = "modules reload")
        old_modules = "`, `".join(self.loader.modules)

        self.loader.unload()
        self.loader.pull()
        self.loader.load()
        
        modules = "`, `".join(self.loader.modules)

        embed.add_field(name = ":heavy_minus_sign: unloaded", value = old_modules)
        embed.add_field(name = ":heavy_plus_sign: loaded", value = modules)
        
        await ctx.respond(embed = embed)

    @group.command(
        name = "list",
        description = "get the list of loaded modules"
    )
    @commands.is_owner()
    async def modules_list(self, ctx: ApplicationContext) -> None:
        description = "`, `".join(self.loader.modules) if len(self.loader.modules) > 1 else f"`{self.loader.modules[0]}`"
        embed = Embed(timestamp = datetime.now(), title = "modules", description = description)
        
        await ctx.respond(embed = embed)


def load(bot: commands.Bot, directory: str, repository: str | None = None) -> None:
    bot.add_cog(LoaderCog(bot, directory, repository))
