import discord
from discord.ext import commands

token = open("config.json", "r").read()
bot = commands.Bot()

@bot.event
async def on_ready() -> None:
  print(bot.user.name, "is ready")

@bot.slash_command(
  name = "dire",
  description = "Fais dire quelque chose au robot."
)
@commands.has_permissions(administrator = True)
async def say(
  ctx: discord.application_command(), 
  message: discord.Option(str)
) -> None:
  await ctx.delete()
  await ctx.channel.send(message)

bot.run(token)
