from discord.ext import commands
from discord import SlashCommandGroup, Embed, ApplicationContext
from datetime import datetime

from .loader import Loader
    

class LoaderInterfaceCog(commands.Cog):
    def __init__(self, bot: commands.Bot, loader: Loader) -> None:
        self.bot: commands.Bot = bot

        self.loader: Loader = loader
        self.loader.load()
        
    group = SlashCommandGroup("modules")

    @group.command(
        name = "update",
        description = "download modules from repository"
    )
    @commands.is_owner()
    async def modules_update(self, ctx: ApplicationContext) -> None:
        embed = Embed(timestamp = datetime.now(), title = "modules reload")
        old_modules = "`, `".join(list(self.loader.modules.keys()))

        self.loader.update()
        
        modules = "`, `".join(list(self.loader.modules.keys()))

        embed.add_field(name = ":heavy_minus_sign: unloaded", value = old_modules)
        embed.add_field(name = ":heavy_plus_sign: loaded", value = modules)
        
        await ctx.respond(embed = embed)

    @group.command(
        name = "list",
        description = "get the list of loaded modules"
    )
    @commands.is_owner()
    async def modules_list(self, ctx: ApplicationContext) -> None:
        description = "`" + "`, `".join([module.__name__ for module in self.loader.modules]) + "`"
        embed = Embed(timestamp = datetime.now(), title = "modules", description = description)
        
        await ctx.respond(embed = embed)

    @group.command(
        name = "reload",
        description = "reload all modules"
    )
    @commands.is_owner()
    async def modules_update(self, ctx: ApplicationContext) -> None:
        self.loader.unload()
        self.loader.load()

        await self.modules_list(ctx)


def load(bot: commands.Bot, directory: str, repository: str | None = None, **kwargs) -> None:
    loader: Loader = Loader(bot, directory, repository, **kwargs)
    bot.add_cog(LoaderInterfaceCog(bot, loader))
