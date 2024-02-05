from discord import application_command, Option, Interaction
from discord.ext import commands
from logging import basicConfig, StreamHandler, FileHandler, DEBUG, INFO, WARN, ERROR, log
from sys import stdout
from os import environ

token = environ["TOKEN"]
print(environ, token)
bot = commands.Bot()

basicConfig(
  level = DEBUG,
  format = "%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d]: %(message)s",
  handlers = [
    FileHandler(
      filename = "discord.log",
      encoding = "utf-8",
      mode = "a"
    ),
    StreamHandler(stdout)
  ]
)

@bot.event
async def on_ready() -> None:
  log(INFO, f"{bot.user.name} now ready.")

@bot.slash_command(
  name = "dire",
  description = "Fais dire quelque chose au robot."
)
@commands.has_permissions(administrator = True)
async def say(
  ctx: application_command(), 
  message: Option(str)
) -> None:
  await ctx.delete()
  await ctx.channel.send(message)

bot.run(token)