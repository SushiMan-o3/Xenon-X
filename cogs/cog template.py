import discord
import random
from discord.ext import commands

def colour():
    colours = [0x921cff, 0x00ff7f, 0xff9b38, 0xff0000, 0x0900ff]
    return random.choice(colours)  

class template(commands.Cog, name='template'):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(template(bot))