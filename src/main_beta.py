import discord
from discord import application_command, Option, Embed, Color
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


def embed(titre, description, auteur):
    embed = discord.Embed(title=titre, description=description, color=discord.Color.random())
    embed.add_field(name="Champ 1", value="Valeur 1")
    embed.set_footer(text="Pied de page de l'embed")
    embed.set.image(url="data:image/png;base64,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")
    embed.set_author(name=auteur)
    return embed

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
    name="embed",
    description="Crée un embed" 
)
async def embed(ctx, Titre: Option(str), Description: Option(str)):
    await ctx.delete()
    embed = embed(Titre, Description, ctx.author.name)
    await ctx.channel.send(embed=embed)

                           
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
async def infos(ctx):
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
    await ctx.respond(f"Commandes Disponible : \n `/ping` - Avoir le ping du bot \n `/infos` - Avoir des Informations sur le bot \n `/help` - Liste des commandes disponibles \n `/say` - Fais dire quelque chose au bot (admin only)")

bot.run(token)
