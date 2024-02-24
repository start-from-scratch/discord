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

@bot.event
async def on_message_delete(message):
    if message.mentions:
        for user in message.mentions:
            channel = bot.get_channel(message.channel.id)
            await user.send(f"Vous avez été ghost ping par {message.author.name} dans le salon {channel.name} du serveur {message.guild.name}")
            await channel.send(f"{user.mention} vous avez été ghost ping par {message.author.mention}")


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
    await ctx.respond(f"{bot.user.mention} ping is {int(bot.latency * 1000)} ms \n A été lancé <t:{start}:R> \n Actuellement dans {len(bot.guilds)} serveurs \n Requested by: {ctx.author.mention}")

@bot.slash_command(
    name = "ping",
    description = "Avoir le ping du bot" 
)
async def status(ctx):
    await ctx.respond(f"{bot.user.mention} ping is {int(bot.latency * 1000)} ms")

@bot.slash_command(
    name = "help",
    description = "Liste des commandes disponibles" 
)
async def help(ctx):
    help_message = "Commandes disponibles : \n"
    for command in bot.commands:
      help_message += f"`/{command.name}` - {command.description} \n"
    await ctx.respond(help_message)


bot.run(token)
