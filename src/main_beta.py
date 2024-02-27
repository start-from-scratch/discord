from discord import application_command, Option, Embed, Colour, Activity, ActivityType, Intents, Message
from discord.ext import commands
from logger import logger
from datetime import datetime
from json import load as json_load
from time import time

config = json_load(open("config.json", "r"))
  
start = int(time())  
start_date = datetime.fromtimestamp(start)
bot = commands.Bot(intents = Intents.all())
bot.remove_command("help")

def create_embed(title: str, description: str, author: str, color: Colour):
    embed = Embed(title=title, description=description, colour=color)
    embed.set_footer(text=f"Informations demandées par : {author}")
    return embed

@bot.event
async def on_ready() -> None:
  logger.info(f"Logged in as {bot.user.name}.")

  for channel_id in config["status_channel_id"]:
    await bot.get_channel(channel_id).send(f"Le bot est connecté en tant que {bot.user.mention} :green_circle: (Version Beta)")

  await bot.change_presence(
    activity = Activity(
      type = ActivityType.watching,
      name = f"{len(bot.guilds)} serveurs"
    )
  )

@bot.event
async def on_message_delete(ctx: Message) -> None:
  if len(ctx.mentions) == 0: return

  if True in [
    ctx.mentions[0] == ctx.author and len(ctx.mentions) == 1, 
    ctx.author.bot,
    ctx.mentions[0].bot and len(ctx.mentions) == 1
  ]: return
  
  embed = Embed(title = "Ghost ping", timestamp = ctx.created_at, colour = Colour.random())
  embed.add_field(name = "Auteur" , value = ctx.author.mention)
  embed.add_field(name = "Message", value = ctx.content)
  embed.add_field(name="Salon:", value=f"ID: {ctx.channel.id} \n Nom: <#{ctx.channel.id}>", inline = False)
  await ctx.channel.send(embed = embed)

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
    name = "infos",
    description = "Avoir des Informations sur le bot" 
)
async def infos(ctx: application_command()):
    embed = create_embed("Infos", f"Le ping du bot {bot.user.mention} est de {int(bot.latency * 1000)}ms \n A été lancé <t:{start}:R> | Le : {start_date} \n Actuellement dans {len(bot.guilds)} serveur(s)", ctx.author.name, 0x008FFF)
    await ctx.respond(embed=embed)

@bot.slash_command(
    name = "ping",
    description = "Avoir le ping du bot" 
)
async def ping(ctx: application_command()) -> None:
    embed = create_embed("Ping", f"Le ping du bot {bot.user.mention} est de {int(bot.latency * 1000)}ms", ctx.author.name, 0xFFA900)
    await ctx.respond(embed=embed)

@bot.slash_command(
    name = "help",
    description = "Liste des commandes disponibles" 
)
async def help(ctx: application_command()) -> None:
    embed = create_embed("Help", f"Commandes Disponible : \n `/ping` - Avoir le ping du bot \n `/infos` - Avoir des Informations sur le bot \n `/help` - Liste des commandes disponibles \n `/say` - Fais dire quelque chose au bot (admin only) \n `/embed` - Crée un embed", ctx.author.name, 0x200B9C)
    await ctx.respond(embed=embed)

@bot.slash_command(
    name= "embed",
    description="Crée un embed" 
)
async def embed(
  ctx: application_command(), 
  titre: Option(str), 
  description: Option(str),
) -> None:
  embed = create_embed(titre, description, ctx.author.name,0x093156)
  await ctx.respond(embed=embed)

@bot.slash_command(
  name= "serveur",
  description="Avoir des informations sur le serveur" 
)
async def serveur(ctx: Message) -> None:
  roles_list = " | ".join((f"<@&{role.id}>" for role in ctx.guild.roles))
  embed = create_embed(f"Infos du serveur {ctx.guild.name}", f"Crée le {ctx.guild.created_at} \n Nombre de Membres: {ctx.guild.member_count} \n Proprietaire : {ctx.guild.owner} \n Nombre de salon textuels: {len(ctx.guild.text_channels)}, Nombre de salon vocaux: {len(ctx.guild.voice_channels)}, Nombre de Roles: {len(ctx.guild.roles)} \n Roles: {roles_list}", ctx.author.name,0x1DB747)
  await ctx.respond(embed=embed)

bot.run(config["token"])
