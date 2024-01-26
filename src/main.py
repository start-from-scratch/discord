from dotenv import load_dotenv
from os import getenv
from sys import argv
from json import loads as json_loads
from discord import Intents
from discord.ext import commands

load_dotenv() 
path = argv[0][:len(argv[0]) - list(reversed(list(argv[0]))).index("/") - 1]

file = open(path + "/../config.json", "r")
config = json_loads(file.read())

bot = commands.Bot(command_prefix=config.get("prefix"), intents=Intents.all())
token = getenv("TOKEN")

@bot.event
async def on_ready() -> None:
    print(bot.user.name, "is ready")

@bot.command(name="say")
@commands.has_permissions(administrator = True)
async def say(ctx, *content: str) -> None:
  await ctx.message.delete()
  await ctx.channel.send(" ".join(content))

bot.run(token)
