from discord.ext import commands
from discord import application_command
from disk import tree
from os.path import dirname
from logging import getLogger

logger = getLogger()

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
        self.load()

        extensions = "`, `".join(self.extensions)
        await ctx.respond(f"Loaded `{extensions}`.")

def setup(bot: commands.Bot) -> None:
    bot.add_cog(Extender(bot))