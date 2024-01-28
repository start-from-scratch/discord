from dotenv import load_dotenv
from os import getenv
from sys import argv
from json import loads as json_loads
from discord import Intents, Embed
from discord.ext import commands
import time


uptime = 0

load_dotenv() 
path = argv[0][:len(argv[0]) - list(reversed(list(argv[0]))).index("/") - 1]

file = open(path + "/../config.json", "r")
config = json_loads(file.read())

bot = commands.Bot(command_prefix=config.get("prefix"), intents=Intents.all())
token = getenv("TOKEN")

@bot.event
async def on_ready() -> None:
    global uptime
    print(bot.user.name, "is ready")
    uptime = round(time.time())        #mettre la variable uptime au timestamp de demarage 
    await bot.get_channel(1201190228233310248).send(f"Bot {bot.user.mention} demarré :green_circle: ") #mettre votre id de salon ou va etre envoyer quand le bot est allumé

@bot.command(name="say")
@commands.has_permissions(administrator = True)
async def say(ctx, *content: str) -> None:
  await ctx.message.delete()
  await ctx.channel.send(" ".join(content))
  
@bot.command(name = "status")
@commands.has_permissions(administrator = True)
async def status(ctx):
    global uptime
    await ctx.message.delete()    # supprimer le message de la commande
    print(f"Test request by: {ctx.author} in {ctx.guild.name}") # écrire dans la console qui a fait la commande
    await ctx.channel.send(f"{bot.user.mention} ping is {ping(ctx.message.created_at.timestamp())} ms | Uptime: <t:{uptime}:R>")
    await ctx.channel.send(f"Requested by: {ctx.author.mention}")  # ping le mec qui a fait la commande

def ping(message_timestamp):
    ping = round((time.time() - message_timestamp) * 1000)
    print(f"Ping du bot {bot.user.name} : {ping}")
    return ping

bot.run(token)

