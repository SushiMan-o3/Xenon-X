from discord.ext import commands
import discord
import os

from config import token

description = "A bot made by a dumbass!"

intents = discord.Intents.default()
intents.members = True 

bot = commands.Bot(command_prefix='!', description=description, intents = intents)

@bot.event
async def on_ready():
    print("ready")

@bot.event
async def on_command_error(ctx, error):
    error_logs = bot.get_channel(750703265783611484)
    await error_logs.send(f"```py\n{error}\n```")
 
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"

cogs = [
    'cogs.important',
    'cogs.other',
    'cogs.server',
    'cogs.currency',
    'jishaku'
    #'cogs.moderation'
]

for cog in cogs:
    bot.load_extension(cog)

bot.run(token)
