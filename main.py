import discord
from discord import Option, Embed, Colour, Intents, Message, Game
from discord.ext import commands, tasks
from utils.logging import logger
from json import load as json_load
from time import time
from random import choice as rchoice, randint
from datetime import datetime
from cogs import loader as cogs

config = json_load(open("config.json", "r"))
start = int(time())
version = "0.0.0"

bot = commands.Bot(intents = Intents.all())
cogs.setup(bot)

bot.remove_command("help")

def create_embed(title: str, description: str, author: str, color: Colour):
    embed = Embed(title=title, description=description, colour=color)
    embed.set_footer(text=f"Informations demandées par: {author}")
    return embed

@tasks.loop(minutes=10)
async def change_activity():
    bot.changeable_activites = [f"être sur {len(bot.guilds)} serveurs", f"regarde la version {version}", "regarder Start from Scratch", "Apex Legends", "Minecraft", "regarder netflix avec Katsuki", "regarder loyds44", "coder", "discuter avec des utilisateurs", "écouter de la musique", "aider les utilisateurs", "analyser des données", "apprendre de nouvelles choses", "aller à la salle", "se rappeler de scratch on scratch", "écouter de la hardbass", "quelquechose avec quelqu'un"]
    await bot.wait_until_ready()
    await bot.change_presence(activity=Game(rchoice(bot.changeable_activites))) 

@bot.event
async def on_ready() -> None:
  logger.info(f"Logged in as {bot.user.name}.")

  for channel_id in config["status_channel_ids"]:
    await bot.get_channel(channel_id).send(f"Le bot est connecté en tant que {bot.user.mention} :green_circle:")

  change_activity.start()

@bot.slash_command(
  name = "say",
  description = "Fais dire quelque chose au bot. (admin only)"
)
@commands.has_permissions(administrator = True)
async def say(ctx, message: Option(str)) -> None:
  await ctx.delete()
  await ctx.channel.send(message)

@bot.slash_command(
  name = "dm",
  description = "Envoie un DM à un utilisateur. (admin only)"
)
@commands.has_permissions(administrator = True)
async def dm(ctx, member: Option(discord.Member, description="Mentionne le membre"), message: Option(str, description="Message a envoyer en privé")) -> None:
  await ctx.delete()
  embed= Embed(title="Nouveau message", description=message,colour=0x093156)
  embed.set_footer(text=f"Message envoyé a partir du serveur {ctx.guild.name}")
  await member.send(embed=embed)

@bot.slash_command(
    name = "infos",
    description = "Avoir des informations sur le bot" 
)
async def infos(ctx):
    embed = Embed(title="Infos",description=f"Information sur le bot {bot.user.mention}", colour= 0x008FFF)
    embed.add_field(name="Données", value=f"Le ping du bot {bot.user.mention} est de {int(bot.latency * 1000)}ms \n A été lancé le <t:{start}:F> (<t:{start}:R>)", inline=False)
    embed.add_field(name="Serveurs", value=f"Actuellement dans {len(bot.guilds)} serveur(s) \n Regarde {sum(guild.member_count for guild in bot.guilds)} membre(s)", inline=False)
    embed.set_footer(text=f"Crée par Loyds44 & Switchcodeur , Version {version}")  #ligne a changé si pas les memes personnes qui ont fait le bots
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
  name= "tirage_de_des",
  description="Faire un lancer de dés" 
)
async def tiragedes(
    ctx, 
    valeur1: Option(int, description="Valeur minimale"),
    valeur2: Option(int, description="Valeur maximale"),
    tirage: Option(int, description="Nombre de lancers")
) -> None:
    embed = Embed(
        title="Lancer de dés",
        description=f"Tirage de {tirage} dés compris entre {valeur1} et {valeur2}.",
        color=Colour.green()
    )
    if valeur1 < valeur2 : 
      for x in range(int(tirage)):
          embed.add_field(
              name=f"Tirage n°{x+1}", 
              value=str(randint(valeur1, valeur2)), 
              inline=True
          )
      await ctx.respond(embed=embed)
    else: 
      await ctx.respond(f"La valeur 1 ({valeur1}) ne peut pas etre inferieur à la valeur 2 ({valeur2})")

@bot.slash_command(
  name = "help",
  description = "Liste des commandes disponibles" 
)
async def help(ctx) -> None:
  embed = Embed(description = "Liste des commandes disponibles", timestamp = datetime.now())
  embed.set_author(name = bot.user.display_name, icon_url = bot.user.display_avatar)
  embed.add_field(name="Ressources",value = "[Serveur support]()",inline=False)
  embed.add_field( name = "Commandes", value = "\n".join([f"`{command.name}` - {command.description}" for command in list(bot.all_commands.values())[1:]]), inline= False)

  await ctx.respond(embed = embed)

@bot.slash_command(
  name= "serveur",
  description="Avoir des informations sur le serveur" 
)
async def serveur(ctx) -> None:

#limite le nbr de roles affiche :
  if len(ctx.guild.roles) >= 36:
    nbr_role = int(len(ctx.guild.roles))-35
    roles_list = ", ".join((role.mention for role in list(reversed(ctx.guild.roles[nbr_role:]))))
    roles_list += f" **et {nbr_role-1} rôles en plus**" 
  else :
    roles_list = ", ".join((role.mention for role in list(reversed(ctx.guild.roles[1:]))))
  
  #creation embed :
  embed = create_embed(ctx.guild.name, f"Information sur le serveur {ctx.guild.name} (`{ctx.guild.id}`)", ctx.author.name, 0x1DB747)
  embed.add_field(name="Création du serveur:", value=f"<t:{int(ctx.guild.created_at.timestamp())}:F>", inline = True)
  embed.add_field(name="Proprietaire:", value=f"{ctx.guild.owner.mention} (`{ctx.guild.owner.id}`)", inline = True)
  embed.add_field(name=f"{len(ctx.guild.roles)-1} rôles:", value=roles_list, inline = False) #le -1 permet de ne pas prendre en compte everyone ds le compte
  embed.add_field(name="Statistiques:",value=f"Nombre de membres: {ctx.guild.member_count} \n Nombre de salons textuels: {len(ctx.guild.text_channels)} \n Nombre de salons vocaux: {len(ctx.guild.voice_channels)}", inline = False) #bot.all_commands.values()[1:] pour ne plus avoir l'affiche de "module"
  await ctx.respond(embed=embed)

@bot.slash_command(
  name = "membre",
  description = "Avoir des informations sur un membre " 
)
async def membre(ctx, member: Option(discord.Member, description="Mentionne le membre")) -> None:
 
 #limite le nbr de roles affiche :
  if len(member.roles) >= 11:
    nbr_role = int(len(member.roles))-10 
    role_names = ", ".join((role.mention for role in list(reversed(member.roles[nbr_role:])))) # Permet d'avoir tous les rôles sauf everyone = ", ".join((role.mention for role in list(reversed((member.roles[nbr_role:]))))
    role_names += f" **et {nbr_role-1} rôles en plus**" 
  else :
   role_names = ", ".join([role.mention for role in list(reversed(member.roles[1:]))]) # Permet d'avoir tous les rôles sauf everyone = ", ".join([role.mention for role in list(reversed(member.roles[1:]))]) # Permet d'avoir tous les rôles sauf everyone

#badges de "status" :
  emoji = ""
  if member.id == ctx.guild.owner.id:
    emoji += ":crown:" #couronne - <:owner_badge:1262777459242172506>
  if any(role.permissions.administrator for role in member.roles) :
    emoji += ":shield:"
  if member.bot:
    emoji += ":robot:"
  if member.id in config["dev_id"] :
    emoji += ":tools:"
  if not emoji :
    emoji = ":bust_in_silhouette:"
  
# Définir l'URL de l'avatar, ou utiliser l'avatar par défaut si None
  avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

#affichage des badges (nitro,maison....)
  emoji_badges = {
    "hypesquad_balance": "<:discord_balance:1262774434008399892>",
    "hypesquad_bravery": "<:discord_bravery:1262774436193505411>",
    "hypesquad_brilliance": "<:discord_brillance:1262774437187424278>",
    "active_developer": "<:developpeur_badge:1262777455609909361>" 
    }
  
  if not member.public_flags.all() : 
    badges_names ="_Aucun Badges_"
  else : 
    badges_names = ", ".join([emoji_badges.get(flag.name, flag.name) for flag in list(member.public_flags.all())])


#creation embed :
  embed = create_embed(None, f"Informations sur le membre {member.mention} {emoji} (`{member.id}`)", ctx.author.name, 0x0193C6)
  embed.set_author(name=member.display_name, icon_url=avatar_url)
  embed.add_field(name="Création du compte :", value=f"<t:{int(member.created_at.timestamp())}:F>", inline=True)
  embed.add_field(name="A rejoint le serveur le :", value=f"<t:{int(member.joined_at.timestamp())}:F>", inline=True)
  embed.add_field(name=f"{len(member.roles)-1} rôles :", value=role_names, inline=False) # -1 car on ne compte pas everyone dans les rôles
  embed.add_field(name=f"Badges", value=badges_names, inline=False)
  embed.set_thumbnail(url=avatar_url)
  await ctx.respond(embed=embed)

@bot.slash_command(
name = "avatar",
description = "Avoir la photo de profil d'un membre" 
)
async def avatar(ctx, member: Option(discord.Member, description="Mentionne le membre")) -> None:

  avatar_url = member.avatar.url if member.avatar else member.default_avatar.url # Définir l'URL de l'avatar, ou utiliser l'avatar par défaut si None

  embed = Embed(title=f"Avatar de {member.display_name}",url= avatar_url)
  embed.set_image(url=avatar_url)
  await ctx.respond(embed=embed)


@bot.slash_command(
  name = "role",
  description = "Avoir des informations sur un rôle" 
)
async def role(ctx, role: Option(discord.Role, description="Mentionne le role")) -> None:
  liste_membre = ", ".join(member.mention for member in role.members[:10])
  if len(role.members) >= 10:
    liste_membre += f" **et {int(len(role.members))-10} membres en plus**" 
  embed = create_embed(None, f"Informations sur le rôle {role.mention} (`{role.id}`)", ctx.author.name, role.color)
  embed.add_field(name="Création du rôle:", value=f"<t:{int(role.created_at.timestamp())}:F>", inline=True)
  embed.add_field(name= f"{len(role.members)} Membres: ", value= liste_membre, inline= False)
  await ctx.respond(embed=embed)

@bot.slash_command(
  name = "emoji",
  description = "Avoir des informations sur un emoji" 
)
async def emoji(ctx, emoji: Option(discord.Emoji, description="Mentionne l'emoji")) -> None:

  embed = create_embed(None, f"Informations sur l'emoji '{emoji.name}' (`{emoji.id}`)", ctx.author.name, 0xE47703)
  embed.set_author(name=emoji.name, icon_url=emoji.url)
  embed.add_field(name="Création de l'emoji:", value=f"<t:{int(emoji.created_at.timestamp())}:F>", inline=True)
  embed.add_field(name="Tag:", value=f"`<:{emoji.name}:{emoji.id}>`", inline=True)
  embed.set_thumbnail(url=emoji.url)
  await ctx.respond(embed=embed)


@bot.slash_command(
  name = "liste_serveurs",
  description = "Avoir la liste des serveurs du bot. (dev only)" 
)
async def liste_serveurs(ctx) -> None:
  if ctx.author.id in config["dev_id"] :
    embed = Embed(title='', description=f"liste des serveurs du bot {bot.user.name}", colour=0x0A3D7D)
    embed.add_field(name=f"{len(bot.guilds)} Serveurs :", value= " \n ".join([guild.name for guild in bot.guilds]), inline=True)
    embed.add_field(name="ID :", value= " \n ".join([str(guild.id) for guild in bot.guilds]), inline=True)
    embed.add_field(name="Membres :", value= " \n ".join([str(guild.member_count) for guild in bot.guilds]), inline=True)
    await ctx.respond(embed=embed)
  else : 
    await ctx.respond("Vous n'etes pas un developpeur du bot, vous ne pouvez donc pas effectuer cette commande")


bot.run(config["token"])