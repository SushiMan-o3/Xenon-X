import discord
import random
from discord.ext import commands
import math
import datetime
import json
import praw
from config import reddit
now = datetime.datetime.now()

def colour():
    colours = [0x921cff, 0x00ff7f, 0xff9b38, 0xff0000, 0x0900ff]
    return random.choice(colours)  

class other(commands.Cog, name='other'):
    def __init__(self, bot):
        self.bot = bot
        
    """
    SMART
    """
    @commands.command(aliases = ['math' , 'm'])
    async def bmath(self, ctx, * , operations=None):
        if operations is None:
            embed=discord.Embed(description='Send the math question you want me to solve!')
            await ctx.send(embed=embed)
        else:
            if '^' in operations:
                operation = operations.replace("^", "**")
            else:
                operation = operations
            answer = eval(operation)
            embed=discord.Embed(title="Math Calculation", description=f'{operations} = {answer}', color=colour())
            await ctx.send(embed=embed)

    @commands.command(aliases = ['sqrt' , 'square root'])
    async def math_sqrt(self, ctx, kwarg):
        if kwarg is None:
            embed=discord.Embed(description='Send the number you want me to square root!')
            await ctx.send(embed=embed)
        else:
            try:
                question = int(kwarg)
                answer = math.sqrt(question)
                embed=discord.Embed(title='Square Roots', description=f"√{question} = {answer}", color=colour())
                await ctx.send(embed=embed)
            except:
                await ctx.send("Something went wrong!")
    
    """O
    ther
    """
    @commands.command(description = "Creates a poll")
    @commands.has_role('Staff')
    async def poll(self, ctx, *, arg, amountt=1):
        try:
            await ctx.channel.purge(limit=amountt)
            msg = await ctx.send(arg)
            for emoji in ("<:yes:779913676533661726>", "<:no:779913676102041651>"):
                await msg.add_reaction(emoji)
        except commands.CheckFailure:
            await ctx.send("You need staff for this.")

    @commands.command(description = "Shows you're away")
    async def afk(self, ctx):
        try:
            nickname = ctx.author.display_name 
            afk = f'[AFK] {nickname}'
            await ctx.author.edit(nick=afk)
            await ctx.channel.send(f'{ctx.author} has gone AFK')
            await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            await ctx.author.edit(nick=nickname)
            await ctx.channel.send(f'{ctx.author.mention} was removed from AFK')
        except commands.BotMissingPermissions:
            embed=discord.Embed(description="The bot needs to have a higher role for you to go into AFK.", color=colour())
            await ctx.send(embed=embed)
    

    @commands.group(invoke_without_command=True)
    async def tag(self, ctx, *, tag: str = None):
        tag = tag.lower()
        with open('cogs/tags.json') as f:
            tags = json.load(f)
        if tag is None:
            await ctx.message.delete(delay=10.0)
            message = await ctx.send('You need to pass a tag.')
            return await message.delete(delay=10.0)
        else:
            if tag not in tags.keys():
                await ctx.message.delete(delay=10.0)
                message = await ctx.send('Could not find a tag with that name.')
                return await message.delete(delay=10.0)
            else:
                await ctx.send(tags[tag])

    @tag.command()
    async def create(self, ctx, * , name: str = None):
        if name is None:
            await ctx.send("The title of the tag you're trying to create is missing.")
        else:
            with open('cogs/tags.json') as f:
                tags = json.load(f)
            if name.lower() in tags.keys():
                await ctx.send("There's a tag with that name!")
            else:
                await ctx.send("Send the description of the tag.")
                description = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                tags[name.lower()] = description.content
                with open('cogs/tags.json', 'w') as f:
                    json.dump(tags, f, indent = 4)
                await ctx.send(f"Done! Your tag has been created.")

    @tag.command()
    async def edit(self, ctx, *, tag: str == None):
        if tag is None:
            await ctx.send('Please specify the tag you want to edit.')
        else:
            with open('cogs/tags.json') as f:
                tags = json.load(f)
            if tag.lower() not in tags.keys():
                await ctx.send("The tag you're trying to edit isn't found.")
            else:
                await ctx.send('What is the new description of this tag?')
                description = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
                tags[tag.lower()] = description.content
                with open('cogs/tags.json', 'w') as f:
                    json.dump(tags, f, indent = 4)
                await ctx.send("Tag edited! Your tag has been edited.")
    
    @tag.command()
    async def delete(self, ctx, *, tag: str == None):
        if tag is None:
            await ctx.send('Please specify the tag you want to delete.')
        else:
            with open('cogs/tags.json') as f:
                tags = json.load(f)
            tag = tag.lower()
            if tag not in tags:
                await ctx.send("The tag that you're trying to delete wasn't found")
            else:
                tags.pop(tag)
                await ctx.send("Tag deleted! Your tag has been deleted.")
                with open('cogs/tags.json', 'w') as f:
                    json.dump(tags, f, indent = 4)
        ...
        ...

    """
    Starboard
    """   
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, reaction):
        pins = self.bot.get_channel(733744363653431387)
        if str(reaction.emoji) == ("📌"):
            channel = await self.bot.fetch_channel(reaction.channel_id)
            message = await channel.fetch_message(reaction.message_id)
            reactors = len(message.reactions)
            if reactors == 3:
                if not message.attachments:
                    embed=discord.Embed(title='Pinned Message', description=message.content, color=colour())
                    embed.set_author(name=f'From: {message.author}', icon_url=message.author.avatar_url)
                    embed.add_field(name=f"Original", value=f"[Jump!]({message.jump_url})")
                    embed.set_footer(text=f'{now.day}/{now.month}/{now.year}')
                    await pins.send(embed=embed)
                else:
                    embed=discord.Embed(title='Pinned Message', description=message.content, color=colour())
                    embed.set_author(name=f'From: {message.author}', icon_url=message.author.avatar_url)
                    embed.add_field(name=f"Original", value=f"[Jump!]({message.jump_url})")
                    embed.set_footer(text=f'{now.day}/{now.month}/{now.year}')
                    embed.set_image(url=message.attachments[0].proxy_url)
                    await pins.send(embed=embed)
    
    @commands.command()
    @commands.has_role('Staff')
    async def pin(self, ctx, id:int):
        if id is None:
            embed=discord.Embed(description = 'Please send me the message id of the message you want me to pin!')
            await ctx.send(embed=embed)
        else:
            pins = self.bot.get_channel(733744363653431387)
            channel = await self.bot.fetch_channel(ctx.channel.id)
            message = await channel.fetch_message(id)
            if not message.attachments:
                embed=discord.Embed(title='Pinned Message', description=message.content, color=colour())
                embed.set_author(name=f'From: {message.author}', icon_url=message.author.avatar_url)
                embed.add_field(name=f"Original", value=f"[Jump!]({message.jump_url})")
                embed.set_footer(text=f'{now.day}/{now.month}/{now.year}')
                await pins.send(embed=embed)
            else:
                embed=discord.Embed(title='Pinned Message', description=message.content, color=colour())
                embed.set_author(name=f'From: {message.author}', icon_url=message.author.avatar_url)
                embed.add_field(name=f"Original", value=f"[Jump!]({message.jump_url})")
                embed.set_footer(text=f'{now.day}/{now.month}/{now.year}')
                embed.set_image(url=message.attachments[0].proxy_url)
                await pins.send(embed=embed)
    
    """
    fun
    """
    @commands.command(aliases = ['reddit', 'breddit'])
    async def browsereddit(self, ctx, *, arg):
        try:
            request = reddit.subreddit(arg)
            one = request.hot(limit=100)
            red_submiss = random.choice(list(one))
            name = red_submiss.title
            link = f"https://reddit.com/{red_submiss.permalink}"
            embed = discord.Embed(
                title = name,
                url = link,
                description = red_submiss.selftext,
                color = 0xFF5700)
            embed.set_image(url = str(red_submiss.url))
            await ctx.send(embed = embed)
        except:
            embed = discord.Embed(description='Subreddit not found!', color=0xFF5700)
            await ctx.send(embed=embed)

    @browsereddit.error
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(description='Please specify a subreddit that you want to search!', color = 0xFF5700)
            await ctx.send(embed=embed)
    
    @commands.command()
    async def redditpost(self, ctx, *, member: discord.Member = None):
        await ctx.send("What is the title of the post?")
        title = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        await ctx.send('What is the description of the post? Add an image if you want.')
        description = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        if not member:
            if not description.attachments:
                embed=discord.Embed(title=title.content, description=description.content, color=0xFF5700)
                embed.set_author(name=f'Posted by u/{ctx.author}', icon_url=ctx.author.avatar_url)
                embed.set_footer(text=f'{now.day}/{now.month}/{now.year}')
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/664231924008484867/729849296333308015/reddit.png')
                bruh = await ctx.send(embed=embed)
                for emoji in ('<:upvote:779913676525404160>', '<:downvote:779913676529729556>'):
                        await bruh.add_reaction(emoji)
            else:
                embed=discord.Embed(title=title.content, description=description.content, color=0xFF5700)
                embed.set_author(name=f'Posted by u/{ctx.author}', icon_url=ctx.author.avatar_url)
                embed.set_footer(text=f'{now.day}/{now.month}/{now.year}')
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/664231924008484867/729849296333308015/reddit.png')
                embed.set_image(url=description.attachments[0].url)
                bruh = await ctx.send(embed=embed)
                for emoji in ('<:upvote:779913676525404160>', '<:downvote:779913676529729556>'):
                        await bruh.add_reaction(emoji)
        else:
            if not description.attachments:
                embed=discord.Embed(title=title.content, description=description.content, color=0xFF5700)
                embed.set_author(name=f'Posted by u/{member}', icon_url=member.avatar_url)
                embed.set_footer(text=f'{now.day}/{now.month}/{now.year}')
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/664231924008484867/729849296333308015/reddit.png')
                bruh = await ctx.send(embed=embed)
                for emoji in ('<:upvote:779913676525404160>', '<:downvote:779913676529729556>'):
                        await bruh.add_reaction(emoji)
            else:
                embed=discord.Embed(title=title.content, description=description.content, color=0xFF5700)
                embed.set_author(name=f'Posted by u/{member}', icon_url=member.avatar_url)
                embed.set_footer(text=f'{now.day}/{now.month}/{now.year}')
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/664231924008484867/729849296333308015/reddit.png')
                embed.set_image(url=description.attachments[0].url)
                bruh = await ctx.send(embed=embed)
                for emoji in ('<:upvote:779913676525404160>', '<:downvote:779913676529729556>'):
                        await bruh.add_reaction(emoji)

    @commands.command()
    async def emoji(self, ctx, *, text: str = None):
        if text is None:
            await ctx.send("Please add the text you want me to convert to emojis.")
        else:
            text = text.lower()
            emojis = {'a':'🇦 ', 'b': '🇧 ', 'c': '🇨 ', 'd': '🇩 ', 'e': '🇪 ', 'f': '🇫 ', 'g': '🇬 ', 'h': '🇭 ', 'i': '🇮 ', 'j': '🇯 ', 'k': '🇰 ', 'l': '🇱 ', 'm': '🇲 ', 'n': '🇳 ', 'o': '🇴 ', 'p': '🇵 ', 'q': '🇶 ', 'r': '🇷 ', 's': '🇸 ', 't': '🇹 ', 'u':'🇺 ', 'v': '🇻 ', 'w': '🇼 ', 'x':'🇽 ', 'y': '🇾 ', 'z': '🇿 ', ' ': '  ', '!': '❗'}
            for i in emojis.keys():
                text = text.replace(i, emojis[i])
            await ctx.send(text)

def setup(bot):
    bot.add_cog(other(bot))
