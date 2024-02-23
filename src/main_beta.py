from discord import application_command, Option, Interaction
from discord.ext import commands
from logging import basicConfig, StreamHandler, FileHandler, DEBUG, INFO, WARN, ERROR, log
from sys import stdout
import time

with open("token.txt", "r") as f:
  token = f.read()
  f.close()

with open("id.txt", "r") as f:
  id = int(f.read())
  f.close()
  
uptime = 0
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

def ping(message_timestamp):
    ping = round((time.time() - message_timestamp) * 1000)
    log(INFO, f"Ping du bot {bot.user.name} : {ping} ms")
    return ping

@bot.event
async def on_ready() -> None:
    global uptime
    uptime = round(time.time())        #mettre la variable uptime au timestamp de demarage 
    log(INFO, f"{bot.user.name} now ready.")
    await bot.get_channel(id).send(f"Bot {bot.user.mention} demarré :green_circle: ") #envoie un msg dans le salon id au demarrage du bot

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
    await ctx.message.delete()    # supprimer le message de la commande
    log(INFO, f"Test request by: {ctx.author} in {ctx.guild.name}") # écrire dans la console qui a fait la commande
    await ctx.channel.send(f"{bot.user.mention} ping is {ping(ctx.message.created_at.timestamp())} ms | Uptime: <t:{uptime}:R> \n Requested by: {ctx.author.mention}")


bot.run(token)
