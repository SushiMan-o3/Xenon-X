from discord.ext import commands
import discord
import json
import random

def colour():
    colours = [0x921cff, 0x00ff7f, 0xff9b38, 0xff0000, 0x0900ff]
    return random.choice(colours)  

class currency(commands.Cog, name='Currency'):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliese = 'help currency')
    async def help_currency(self, ctx):
        ...

    @commands.command(description = "Registers you into our currency system.")
    async def register(self, ctx):
        with open('currency.json') as f:
            balance = json.load(f)
        
        member = str(ctx.author.id)
        
        if member in balance.keys():
            await ctx.send("You are already in the currency system.")
        else:
            balance[str(member)] = int(500)

            with open('currency.json', 'w') as f:
                json.dump(balance, f, indent = 4)
                await ctx.send(f"{ctx.author.mention} is now registered!")

    @commands.command(description="Checks the user's balance!")
    async def balance(self, ctx, *, member: discord.Member = None):
        with open('currency.json') as f:
                    balance = json.load(f)
        if member == None:
            if str(ctx.author.id) not in balance.keys():
                await ctx.send("You haven't registered yet. Use `!register` to register for the currency bot!")
            else:
                embed = discord.Embed(title = "Balance", description = f"{ctx.author.mention} has {balance[str(ctx.author.id)]}", color = colour())
                await ctx.send(embed = embed)
        else:  
            if str(member.id) not in balance.keys():
                await ctx.send("They haven't registered yet. Use `!register` to register for the currency bot!")
            else:
                embed = discord.Embed(title = f"Balance", description = f"{member.mention} has {balance[str(member.id)]}", color = colour() )
                await ctx.send(embed = embed)

    @commands.command(description = "Work's for money")
    @commands.cooldown(1, 60**3, commands.BucketType.user)
    async def work(self, ctx):
        with open('currency.json') as f:
                    balance = json.load(f)
        if str(ctx.author.id) not in balance.keys():
            await ctx.send("You haven't registered yet. Use `!register` to register for the currency bot!")
        else:
            with open('currency.json') as f:
                balance = json.load(f)

            add = 500 + balance[str(ctx.author.id)]

            balance[str(ctx.author.id)] = add

            with open('currency.json', 'w') as f:
                json.dump(balance, f, indent = 4)

            embed = discord.Embed(description = f"{ctx.author.mention} worked and gained $500, and now has ${balance[str(ctx.author.id)]}", color = colour())
            await ctx.send(embed = embed)

    @commands.command(description = "Set's the a person value to a certain amount (OWNER ONLY)")
    async def set(self, ctx, value:int, member: discord.Member = None):
        user_can = [514904785850204211, 371807395816538113, 564484657509302282]
        try:
            if ctx.author.id in user_can:
                if member == None:
                    with open('currency.json') as f:
                        balance = json.load(f)
                    balance[str(ctx.author.id)] = value
                    with open('currency.json', 'w') as f:
                        json.dump(balance, f, indent = 4)
                    await ctx.send(f'{ctx.author.mention} has ${balance[str(ctx.author.id)]}')
                else:
                    with open('currency.json') as f:
                        balance = json.load(f)
                    balance[str(member.id)] = value
                    with open('currency.json', 'w') as f:
                        json.dump(balance, f, indent = 4)

                    await ctx.send(f'{member.mention} has ${balance[str(member.id)]}')
            else:
                await ctx.send("You can't use this command.")
        except:
            await ctx.send('Something is off.')

    @commands.command(description = 'Leader board for who has the most money!')
    async def leaderboard(self, ctx):
        with open('currency.json') as f:
            balance = json.load(f)
        top_5 = sorted(balance, key=balance.get, reverse=True)[:5]
        five_top = []
        for i,e in zip(top_5, range(1, 6)):
            five_top.append(f'{e}. <@!{int(i)}> - ${balance[i]}')
        string = str(five_top)
        x = string.replace(", ", "\n\n")
        for i in "[']": x=x.replace(i,'')
        embed = discord.Embed(title = "Leaderboard - Top 5", description = x, color = colour())
        await ctx.send(embed=embed)

    @commands.command()
    async def buy(self, ctx, *, item: str):
        with open('currency.json') as f:
            balance = json.load(f)
        with open('shop.json') as f:
            shop = json.load(f)
        item = item.lower()
        if item in shop.keys():
            item_price = int(shop[item])
            if str(ctx.author.id) in balance.keys():
                user = balance[str(ctx.author.id)]
                if user < item_price:
                    await ctx.send(f"You don't have enough money to buy {item.title()}!")
                else:
                    balance[str(ctx.author.id)] = user - item_price
                    with open("currency.json", 'w') as f:
                        json.dump(balance, f, indent = 4)
                    await ctx.send(f"You bought the {item.title()}, and it added to your inventory!")
                    #add it into another json file where key = id and a list with all items as a value
                    with open("items.json") as f:
                        items = json.load(f)
                    if str(ctx.author.id) in items.keys():
                        items[str(ctx.author.id)].append(item)
                    else:
                        items[str(ctx.author.id)] = [item]
                    with open("items.json", 'w') as f:
                        json.dump(items, f, indent = 4)
            else:
                await ctx.send("Do `!register` to sign up!")
        else:
            await ctx.send(f'{item.title()} is not in the shop.')

    @commands.command()
    async def inventory(self, ctx):
        with open('items.json') as f:
            items = json.load(f)
        if str(ctx.author.id) not in items.keys():
            await ctx.send("You don't have anything in your inventory. Buy some stuff using !buy <item>")
        else:
            with open('shop.json') as f:
                shop = json.load(f)
            itemsss = []
            for x in shop:
                itemsss.append(f'{(items[str(ctx.author.id)]).count(x)}  {x.title()}') 
            user = (str(itemsss))
            x = user.replace(", ", "\n\n")
            for i in "[']": x=x.replace(i,'')
            embed = discord.Embed(title = 'Items', description = f'*You have...*\n\n {x}', color = colour())
            embed.set_footer(text = f"{ctx.author}'s items")
            await ctx.send(embed=embed)
        

def setup(bot):
    bot.add_cog(currency(bot))