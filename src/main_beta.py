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
    uptime = round(time.time())

@bot.command(name="say")
@commands.has_permissions(administrator = True)
async def say(ctx, *content: str) -> None:
  await ctx.message.delete()
  await ctx.channel.send(" ".join(content))

@bot.command(name= "status")
async def ping(ctx):
   global uptime
   await ctx.message.delete()
   print(f"Test request by : {ctx.author} (commands = ping)")
   embed = Embed(title = "Status", description = f"{bot.user.name} ping is {round(bot.latency)*1000} ms |  Uptime : <t:{uptime}:R>" , color = 0x71368A)
   embed.set_thumbnail(url = ctx.guild.icon_url)
   embed.set_footer(text = f"Requested by {ctx.author}", icon_url = ctx.author.avatar_url)
   await ctx.reply(embed = embed)
   await ctx.send(f"Ping author : {ctx.author.mention}")

bot.run(token)
