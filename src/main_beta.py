from discord import application_command, Option
from discord.ext import commands
from logs import logger
from time import time

with open("token.txt", "r") as f:
  token = f.read()
  f.close()

with open("id.txt", "r") as f:
  id = int(f.read())
  f.close()
  
start = int(time())          #voir uptime 
bot = commands.Bot()

@bot.event
async def on_ready() -> None:
    await bot.get_channel(id).send(f"Bot {bot.user.mention} demarré :green_circle: (Version Beta)") #envoie un msg dans le salon id au demarrage du bot

@bot.slash_command(
  name = "say",
  description = "Fais dire quelque chose au bot."
)
@commands.has_permissions(administrator = True)
async def say(
  ctx: application_command(), 
  message: Option(str)
) -> None:
  await ctx.delete()
  await ctx.channel.send(message)

@bot.slash_command(
    name = "status",
    description = "Avoir des Informations sur le bot" 
)
@commands.has_permissions(administrator = True)
async def status(ctx):
    await ctx.respond(f"{bot.user.mention} ping is {int(bot.latency * 1000)} ms | A été lancé <t:{start}:R> \n Requested by: {ctx.author.mention}")

@bot.slash_command(
    name = "ping",
    description = "Avoir le ping du bot" 
)
@commands.has_permissions(administrator = True)
async def status(ctx):
    await ctx.respond(f"{bot.user.mention} ping is {int(bot.latency * 1000)} ms")


bot.run(token)
