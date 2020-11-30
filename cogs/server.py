import discord
import random
from discord.ext import commands

def colour():
    colours = [0x921cff, 0x00ff7f, 0xff9b38, 0xff0000, 0x0900ff]
    return random.choice(colours)  

class server(commands.Cog, name='server'):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome = self.bot.get_channel(733707871233114252)
        role = discord.utils.get(member.guild.roles, name="Member")

        embed=discord.Embed(description=f'Welcome {member.mention}!', color=colour())
        await welcome.send(embed=embed)
        await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        goodbye = self.bot.get_channel(733734004305428620)
        embed=discord.Embed(description=f'Goodbye {member.mention}!', color=colour())
        await goodbye.send(embed=embed)


def setup(bot):
    bot.add_cog(server(bot))