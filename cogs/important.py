import discord
import random
from discord.ext import commands

def colour():
    colours = [0x921cff, 0x00ff7f, 0xff9b38, 0xff0000, 0x0900ff]
    return random.choice(colours)  

class important(commands.Cog, name='Important'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description = "Check's the bot's ping.")
    async def ping(self, ctx):
        embed = discord.Embed(description=f'Pong! {round(self.bot.latency * 1000)} ms!', color=colour())
        await ctx.send(embed=embed)

    @commands.command(description = 'Invite xenon to your server!')
    async def invite(self, ctx):
        embed=discord.Embed(title='Invite link', description='Click the link below to invite me to your server! \n\n[Invite Link](https://discord.com/oauth2/authorize?client_id=720825208889540709&scope=bot&permissions)', color=colour())
        embed.set_footer(text = f'Requested by: {ctx.author}')
        await ctx.send(embed=embed)

    @commands.command(description = 'Information about the server!')
    async def serverinfo(self, ctx):
        embed=discord.Embed(title="Serverinfo", color=colour())
        embed.add_field(name='Server Name', value =ctx.guild.name, inline=True)
        embed.add_field(name='Owner', value=ctx.guild.owner, inline=True)
        embed.add_field(name='Members', value=ctx.guild.member_count, inline=True)
        embed.add_field(name="Region", value=ctx.guild.region, inline=True)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(description = 'Information about a role')
    async def roleinfo(self, ctx, *, role: discord.Role=None):
        if not role:
            embed=discord.Embed(description='Please specify a role you want to check out!')
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f"Role Info on {role}", color=colour())
            embed.add_field(name='Name', value=role, inline=True)
            embed.add_field(name='Role ID', value=role.id, inline=True)
            embed.add_field(name='Members who have the Role', value=(len(role.members)), inline=True)
            embed.add_field(name='Role Colour', value=role.color, inline=True)
            await ctx.send(embed=embed)

    @roleinfo.error
    async def on_command_error(self, ctx, error):
        if isinstance(error,  commands.BadArgument):
            embed = discord.Embed(description="Role not found!")
            await ctx.send(embed=embed)

    @commands.command(description = 'Information about a person.')
    async def userinfo(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
            embed=discord.Embed(title= f"User Information on @{member}", description=f'{member.mention}', color=colour()) 
            embed.add_field(name= f"Name", value= member, inline=True)
            embed.add_field(name='ID', value=member.id, inline=True)
            embed.add_field(name='Nickname', value=member.nick, inline=True)
            embed.add_field(name='Server', value=f'{ctx.guild.name}', inline=True)
            embed.add_field(name='Status', value=member.status, inline=True)
            embed.add_field(name='Activity', value=member.activity, inline=True)
            embed.add_field(name="Highest Role:", value=member.top_role.mention, inline=True)
            embed.set_thumbnail(url = member.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title= f"User Information on @{member}", description=f'{member.mention}', color=colour()) 
            embed.add_field(name= f"Name", value= member, inline=True)
            embed.add_field(name='ID', value=member.id, inline=True)
            embed.add_field(name='Nickname', value=member.nick, inline=True)
            embed.add_field(name='Server', value=f'{ctx.guild.name}', inline=True)
            embed.add_field(name='Status', value=member.status, inline=True)
            embed.add_field(name='Activity', value=member.activity, inline=True)
            embed.add_field(name="Highest Role:", value=member.top_role.mention, inline=True)
            embed.set_thumbnail(url = member.avatar_url)
            await ctx.send(embed=embed)

    @userinfo.error
    async def on_command_error(self, ctx, error):
        if isinstance(error,  commands.BadArgument):
            embed = discord.Embed(description="Member not found!")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(important(bot))