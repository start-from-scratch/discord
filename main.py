from discord import Option, Embed, Colour, Intents, Message, Game
from discord.ext import commands, tasks
from logs import logger
from json import load as json_load
from time import time
from random import choice as rchoice
import extensions
from datetime import datetime

config = json_load(open("config.json", "r"))
start = int(time())  
bot = commands.Bot(intents = Intents.all())
bot.remove_command("help")
extensions.setup(bot)

def create_embed(title: str, description: str, author: str, color: Colour):
    embed = Embed(title=title, description=description, colour=color)
    embed.set_footer(text=f"Informations demandées par : {author}")
    return embed

@tasks.loop(minutes=10)
async def change_activity():
    bot.changeable_activites = [f"être sur {len(bot.guilds)} serveurs", "regarder Start from Scratch", "Apex Legends", "Minecraft", "regarder loyds44", "coder", "discuter avec des utilisateurs", "écouter de la musique", "aider les utilisateurs", "gérer des statistiques", "analyser des données", "apprendre de nouvelles choses", "aller à la salle", "se rappeler de scratch on scratch", "écouter de la hardbass", "quelquechose avec quelqu'un"]
    await bot.wait_until_ready()
    await bot.change_presence( activity=Game(rchoice(bot.changeable_activites))) 

@bot.event
async def on_ready() -> None:
  logger.info(f"Logged in as {bot.user.name}.")

  for channel_id in config["status_channel_ids"]:
    await bot.get_channel(channel_id).send(f"Le bot est connecté en tant que {bot.user.mention} :green_circle: (Version Beta)")

  change_activity.start()

@bot.slash_command(
  name = "say",
  description = "Fais dire quelque chose au bot."
)
@commands.has_permissions(administrator = True)
async def say(
  ctx, 
  message: Option(str)
) -> None:
  await ctx.delete()
  await ctx.channel.send(message)

@bot.slash_command(
    name = "infos",
    description = "Avoir des Informations sur le bot" 
)
async def infos(ctx):
    embed = create_embed("Infos", f"Le ping du bot {bot.user.mention} est de {int(bot.latency * 1000)}ms \n A été lancé <t:{start}:R> | Le <t:{start}:F> \n Actuellement dans {len(bot.guilds)} serveur(s)", ctx.author.name, 0x008FFF)
    await ctx.respond(embed=embed)

@bot.slash_command(
    name = "ping",
    description = "Avoir le ping du bot" 
)
async def ping(ctx) -> None:
    embed = create_embed("Ping", f"Le ping du bot {bot.user.mention} est de {int(bot.latency * 1000)}ms", ctx.author.name, 0xFFA900)
    await ctx.respond(embed=embed)

@bot.slash_command(
    name= "embed",
    description="Crée un embed" 
)
async def embed(
  ctx, 
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
  roles_list = " | ".join((f"<@&{role.id}>" for role in list(reversed(ctx.guild.roles))[:35]))
  if len(ctx.guild.roles) >= 35:
     roles_list += " **et plus**"
  embed = create_embed(ctx.guild.name, f"Information sur le serveur {ctx.guild.name} (`{ctx.guild.id}`)", ctx.author.name, 0x1DB747)
  embed.add_field(name="Création du serveur:", value=f"<t:{int(ctx.guild.created_at.timestamp())}:F>", inline = True)
  embed.add_field(name="Proprietaire:", value=f"{ctx.guild.owner.mention} (`{ctx.guild.owner.id}`)", inline = True)
  embed.add_field(name=f"{len(ctx.guild.roles)} roles:", value=roles_list, inline = False)
  embed.add_field(name="Statistiques:",value=f"Nombre de membres: {ctx.guild.member_count} \n Nombre de salons textuels: {len(ctx.guild.text_channels)} \n Nombre de salons vocaux: {len(ctx.guild.voice_channels)}", inline = False)
  await ctx.respond(embed=embed)

@bot.slash_command(
  name= "dés",
  description="faire un lancer de des " 
)
async def tiragedes(
  ctx, 
  valeur1: Option(int, description="Valeur minimale"),
  valeur2: Option(int, description="Valeur maximale"),
  tirage: Option(int, description="Nombre de lancers"),
) -> None:
  embed = Embed(
    title = "Lancer de dés",
    description = f"Tirage de {tirage} dés compris entre {valeur1} et {valeur2}.",
    color = Colour.green()
  )

  for x in range(int(tirage)):
    embed.add_field(
      name = f"Tirage n°{x+1}", 
      value = str(randint(valeur1,valeur2)), 
      inline=True
    )

  await ctx.respond(embed=embed)

@bot.slash_command(
  name = "help",
  description = "Liste des commandes disponibles" 
)
async def help(ctx) -> None:
  embed = Embed( 
    description = "Liste des commandes disponibles",
    timestamp = datetime.now(),
  )

  embed.set_author(
    name = bot.user.display_name,
    icon_url = bot.user.display_avatar,
  )

  embed.add_field(
    name = "Commandes",
    value = "\n".join([f"`{command.name}` - {command.description}" for command in bot.all_commands.values()]),
  )

  await ctx.respond(embed = embed)

bot.run(config["token"])
