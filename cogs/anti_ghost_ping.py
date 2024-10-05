from discord.ext import commands
from discord import Message, Embed, Colour, AuditLogAction

from cog import get_cogs

cogs = get_cogs("discord")

@cogs.cog
class AntiGhostPing(commands.Cog):
    def __init__(self, bot: commands.Bot, **kwargs) -> None:
        self.bot = bot
        bot.add_cog(self)

    @commands.Cog.listener()
    async def on_message_delete(self, ctx: Message) -> None:
        if len(ctx.mentions) >= 1 and any([
            ctx.mentions[0] == ctx.author and len(ctx.mentions) == 1,
            ctx.mentions[0].bot and len(ctx.mentions) == 1
        ]): return
        elif any([
            ctx.author.bot,
            ctx.author.guild_permissions.manage_messages,
            ctx.guild.audit_logs(limit=1,action=AuditLogAction.message_delete)[0].user.id != ctx.author.id
        ]): return
        
        embed = Embed(title = "Ghost ping", timestamp = ctx.created_at, colour = Colour.random())
        embed.add_field(name = "Auteur" , value = ctx.author.mention)
        embed.add_field(name = "Message", value = ctx.content)
        embed.add_field(name="Salon:", value=f"ID: {ctx.channel.id}\n Nom: <#{ctx.channel.id}>", inline = False)

        await ctx.channel.send(embed = embed)
