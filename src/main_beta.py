import discord
from discord import application_command, Option, Embed, Color
from discord.ext import commands
from logs import logger
from time import time
from datetime import datetime

with open("token.txt", "r") as f:
  token = f.read()
  f.close()

with open("id.txt", "r") as f:
  id = int(f.read())
  f.close()
  
start = int(time())          #voir uptime 
start_date = datetime.fromtimestamp(start)
bot = commands.Bot()
running = False

#Embed createur
def create_embed(titre, description, auteur, couleur):
    embed = discord.Embed(title=titre, description=description, color=couleur)
    embed.set_footer(text=f"Informations demandées par : {auteur}")
    return embed

#Demarrage du bot
@bot.event
async def on_ready() -> None:
  global running
  if not running:
    running = True
    await bot.get_channel(id).send(f"Bot {bot.user.mention} demarré :green_circle: (Version Beta)")

#Ghost Ping
@bot.event
async def on_message_delete(message):
  if message.author in message.mentions:
    return
  if message.mentions and not message.author.bot:
          for user in message.mentions:
            if not user.bot:
                  channel = bot.get_channel(message.channel.id)
                  await user.send(f"Vous avez été ghost ping par {message.author.name} dans le salon <#{message.channel.id}> du serveur {message.guild.name}")
                  embed = create_embed("Ghost Ping","Un Ghost ping vient d'être détecté", bot.user.name, discord.Color.random())
                  embed.add_field(name="Auteur:", value= message.author.mention, inline = True)
                  embed.add_field(name="Mention:", value=user.mention, inline = True)
                  embed.add_field(name="Salon:", value=f"ID: {message.channel.id} \n Nom: <#{message.channel.id}>", inline = False)
                  await channel.send(embed=embed) 

#Commande Say                           
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

#Commande infos
@bot.slash_command(
    name = "infos",
    description = "Avoir des Informations sur le bot" 
)
async def infos(ctx):
    embed = create_embed("Infos", f"Le ping du bot {bot.user.mention} est de {int(bot.latency * 1000)}ms \n A été lancé <t:{start}:R> le : {start_date} \n Actuellement dans {len(bot.guilds)} serveur(s)", ctx.author.name, 0x008FFF)
    await ctx.respond(embed=embed)

#Commande ping
@bot.slash_command(
    name = "ping",
    description = "Avoir le ping du bot" 
)
async def ping(ctx):
    embed = create_embed("Ping", f"Le ping du bot {bot.user.mention} est de {int(bot.latency * 1000)}ms", ctx.author.name, 0xFFA900)
    await ctx.respond(embed=embed)

#Commande help
@bot.slash_command(
    name = "help",
    description = "Liste des commandes disponibles" 
)
async def help(ctx):
    embed = create_embed("Help", f"Commandes Disponible : \n `/ping` - Avoir le ping du bot \n `/infos` - Avoir des Informations sur le bot \n `/help` - Liste des commandes disponibles \n `/say` - Fais dire quelque chose au bot (admin only) \n `/embed` - Crée un embed", ctx.author.name, 0x200B9C)
    await ctx.respond(embed=embed)

#Commande embed
@bot.slash_command(
    name= "embed",
    description="Crée un embed" 
)
async def embed(ctx, 
  titre: Option(str), 
  description: Option(str),
):
  embed = create_embed(titre, description, ctx.author.name,0x093156)
  await ctx.respond(embed=embed)


#Commande serveur
@bot.slash_command(
    name= "serveur",
    description="Avoir des informations sur le serveur" 
)
async def embed(ctx):
  embed = create_embed(titre, description, ctx.author.name,0x053156)
  await ctx.respond(embed=embed)


bot.run(token)
