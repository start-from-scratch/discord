from discord import application_command, Option, Interaction
from discord.ext import commands
from logging import basicConfig, StreamHandler, FileHandler, DEBUG, INFO, WARN, ERROR, log
from sys import stdout
from os import environ
import time

token = environ["TOKEN"]
print(environ, token)
bot = commands.Bot()
uptime = 0

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

def ping(message_timestamp):
    ping = round((time.time() - message_timestamp) * 1000)
    print(f"Ping du bot {bot.user.name} : {ping} ms")
    return ping

@bot.event
async def on_ready() -> None:
    global uptime
    uptime = round(time.time())        #mettre la variable uptime au timestamp de demarage 
    log(INFO, f"{bot.user.name} now ready.")
    await bot.get_channel(1201190228233310248).send(f"Bot {bot.user.mention} demarré :green_circle: ") #mettre votre id de salon ou va etre envoyer quand le bot est allumé

@bot.slash_command(
  name = "say",
  description = "Fais dire quelque chose au bot."
)
@commands.has_permissions(administrator = True)
async def say(
  ctx: discord.application_command(), 
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
    global uptime
    await ctx.message.delete()    # supprimer le message de la commande
    print(f"Test request by: {ctx.author} in {ctx.guild.name}") # écrire dans la console qui a fait la commande
    await ctx.channel.send(f"{bot.user.mention} ping is {ping(ctx.message.created_at.timestamp())} ms | Uptime: <t:{uptime}:R>")
    await ctx.channel.send(f"Requested by: {ctx.author.mention}")  # ping le mec qui a fait la commande


bot.run(token)
