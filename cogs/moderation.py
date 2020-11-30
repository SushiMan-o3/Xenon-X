from discord.ext import commands
import discord
import random
import datetime
import json
now = datetime.datetime.now()

def colour():
    colours = [0x921cff, 0x00ff7f, 0xff9b38, 0xff0000, 0x0900ff]
    return random.choice(colours)  

class moderation(commands.Cog, name='Moderation'):
    def __init__(self, bot):
        self.bot = bot
            
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = None):
        try:
            logs = self.bot.get_channel(733708136049016882)
            if not amount:
                embed=discord.Embed(description='Please specify an amount that you want to purge')
                await ctx.send(embed=embed)
            else:
                await ctx.channel.purge(limit=amount+1, check=lambda msg: not msg.pinned)
            embed = discord.Embed(title="Purge", description=f'{amount} messages were purged by {ctx.author.mention} in {ctx.channel.mention}', color=0xffffff)
            await logs.send(embed=embed)
        except commands.CheckFailure:
            await ctx.send("You don't have the permission to manage messages.")

    @commands.command()
    @commands.has_role('Staff')
    async def warn(self, ctx, user: discord.Member=None, *, arg=None):
        try:
            logs = self.bot.get_channel(733708136049016882)
            if not user:
                embed=discord.Embed(description='Please mention a member that you want to warn!')
                await ctx.send(embed=embed)
            if not arg:
                embed=discord.Embed(description='Please provide a reason!')
                await ctx.send(embed=embed)
            else:
                
                await ctx.send(f'{user.mention} has been warned')
                try:
                    await user.create_dm()
                    await user.dm_channel.send(f'{user.mention}, you have been warned in {ctx.guild.name} for {arg}!')
                except: 
                    await ctx.send(f"> {user}'s DMs are closed!")
                embed = discord.Embed(title="Warn", description=f'**Reason:** {arg}\n**Member Warned:** {user.mention}\n**Warned by:** {ctx.author.mention}', color=0xffffff)
                await logs.send(embed=embed)
        except commands.CheckFailure:
            await ctx.send("You need to be staff to use this command!")

        """
        @bot.command()
        async def warn(ctx, mention: discord.Member, reason):
            with open('warns.json') as f:
                warns = json.load(f)
            if str(mention.id) not in warns.keys():
                warns[str(mention.id)] = [f'1. {reason}']
                with open('warns.json', 'w') as f:
                    json.dump(warns, f, indent = 4)
                    await mention.send(f'You have been warned in {ctx.guild} for: {reason}')
            else:
                warns[str(mention.id)].append(f'{len(warns[str(mention.id)]) + 1}. {reason}')
                with open('warns.json', 'w') as f:
                    json.dump(warns, f, indent = 4)
                await ctx.send('Warn was logged')
                await mention.send(f'You have been warned in {ctx.guild} for: {reason}')

        @bot.command()
        async def warns(ctx, mention: discord.Member):
            with open('warns.json') as f:
                warns = json.load(f)
            if str(mention.id) not in warns.keys():
                await ctx.send(f"{mention.name} user has 0 warns")
            else:
                user = str(warns[str(mention.id)])
                x = user.replace(", ", "\n\n")
                for i in "[']": x=x.replace(i,'')
                embed = discord.Embed(title = f"{mention.name}'s Warns", description = x, color = 0xffffff)
                await ctx.send(embed=embed)
        """

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member=None, *, reason=None):
        try:
            if not user:
                embed=discord.Embed(description='Please mention a member that you want to kick!')
                await ctx.send(embed=embed)
            if not reason:
                embed=discord.Embed(description='Please provide a reason!')
                await ctx.send(embed=embed)
            else:
                try:
                    logs = self.bot.get_channel(733392614614761473)
                    await user.kick(reason=reason)
                    await ctx.send(f'{user} was successfully kicked!')
                    embed = discord.Embed(title="Kick", description=f'**Reason:** {reason}\n**Member kicked:** {user.mention}\n**kicked by:** {ctx.author.mention}', color=0xffffff)
                    await logs.send(embed=embed)
                except:
                    await ctx.send(f'{user} could not be kicked.')
        except commands.CheckFailure:
            await ctx.send("You don't have the permissions to kick people.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def ban(self, ctx, user: discord.Member=None, *, reason=None):
        try:
            if not user:
                embed=discord.Embed(description='Please mention a member that you want to ban!')
                await ctx.send(embed=embed)
            if not reason:
                embed=discord.Embed(description='Please provide a reason!')
                await ctx.send(embed=embed)
            else:
                try:
                    logs = self.bot.get_channel(733392614614761473)
                    await user.ban(reason=reason)
                    await ctx.send(f'{user} was successfully Banned!')
                    embed = discord.Embed(title="Ban", description=f'**Reason:** {reason}\n**Member Banned:** {user.mention}\n**Banned by:** {ctx.author.mention}', color=0xffffff)
                    await logs.send(embed=embed)
                except:
                    await ctx.send(f'{user} could not be Banned.')
        except commands.CheckFailure:
            await ctx.send("You don't have the permissions to ban people.")

    @commands.command(pass_context = True)
    @commands.has_role('Staff')
    async def mute(self, ctx, member: discord.Member=None, *, reason=None):
        try:
            if not member:
                embed=discord.Embed(description='Please mention a member that you want to mute!')
                await ctx.send(embed=embed)
            else:
                logs = self.bot.get_channel(733474243311829042)
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                await member.add_roles(role)
                em=discord.Embed(description=f'{member.name} was successfully muted!')
                await ctx.send(embed=em)
                embed = discord.Embed(title="Mute", description=f'**Reason:** {reason}\n**Member Muted:** {member.mention}\n**Muted by:** {ctx.author.mention}', color=0xffffff)
                await logs.send(embed=embed)
        except commands.CheckFailure:
            await ctx.send("You need staff for this.")

    @commands.command(pass_context = True)
    @commands.has_role('Staff')
    async def unmute(self, ctx, member: discord.Member=None):
        try:
            if member is None:
                embed=discord.Embed(description='Please mention a member that you want to unmute!')
                await ctx.send(embed=embed)
            else:
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                logs = self.bot.get_channel(733474243311829042)
                await member.remove_roles(role)
                await ctx.send(f'{member.mention} has been unmuted!')
                embed = discord.Embed(title="Unmute", description=f'{member.mention} was unmuted by {ctx.author.mention}', color=0xffffff)
                await logs.send(embed=embed)
        except commands.CheckFailure:
            await ctx.send("You need staff for this.")    

    @commands.Cog.listener()
    async def on_message(self, message):
        logs = self.bot.get_channel(733708136049016882)
        bad_words = ["nigga", "nigger"]
        for word in bad_words:
            if message.content.count(word) > 0:
                await message.channel.purge(limit=1)
                await message.channel.send('Sorry, you cant say that. It might offend some people.')
                embed = discord.Embed(title="Bad Word", description=f'{message.author.mention} said the N-Word', color=0xffffff)
                await logs.send(embed=embed)
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        logs = self.bot.get_channel(733708136049016882)
        if not message.attachments:
            await logs.send(f'Deleted in {message.channel.mention}')
            embed=discord.Embed(title = 'Message Deleted', description = message.content)
            embed.set_author(name=f'From: {message.author}', icon_url=message.author.avatar_url)
            embed.set_footer(text=f'{now.day}/{now.month}/{now.year}')
            await logs.send(embed=embed)
        else:
            await logs.send(f'Deleted in {message.channel.mention}')
            embed=discord.Embed(title = 'Message Deleted', description = message.content)
            embed.set_author(name=f'From: {message.author}', icon_url=message.author.avatar_url)
            embed.set_footer(text=f'{now.day}/{now.month}/{now.year}')
            embed.set_image(url=message.attachments[0].proxy_url)
            await logs.send(embed=embed)
        await self.bot.process_commands(message)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        channel = self.bot.get_channel(733708136049016882)
        if before.author == self.bot.user:
            return
        await channel.send(f'Edited in {before.channel}')
        embed = discord.Embed(description=f"**Message Edited**\n\n**Old**\n```{before.content}```\n\n**New**\n```{after.content}\n```")
        embed.set_author(name = f'From: {before.author}', icon_url= before.author.avatar_url)
        embed.set_footer(text=f'{now.day}/{now.month}/{now.year}')
        await channel.send(embed=embed)
        
def setup(bot):
    bot.add_cog(moderation(bot))