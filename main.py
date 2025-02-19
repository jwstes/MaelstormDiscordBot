import discord
from discord.ext import commands
import aiohttp
import asyncio


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")




@bot.command(name="topup")
async def purchase(ctx):
    if "ticket" not in ctx.channel.name.lower():
        await ctx.send("Please create a ticket and send !topup .")
        return

    user_id = ctx.author.id
    purchase_url = f"https://buy.stripe.com/4gwaFTbhn8MgfvOeUY?client_reference_id={user_id}-NIL"

    embed = discord.Embed(
        title="Add Credits To Key",
        description="Click the button below to complete your purchase!",
        color=0x00ff00
    )
    
    embed.add_field(name="IMPORTANT:", value="You must enter your **Maelstorm Key** during checkout. If you do not already have a key, send **!getkey** to receive one.", inline=False)
    embed.add_field(name="What to do after topping up?", value=f"Download Maelstorm Bypass if you haven't already and validate it using your key. Under the usage section, you should see your current credit balance.", inline=False)

    view = discord.ui.View()
    button = discord.ui.Button(label="Buy Now", style=discord.ButtonStyle.link, url=purchase_url)
    view.add_item(button)

    await ctx.send(embed=embed, view=view)


@bot.command(name="bundle1")
async def purchase(ctx):
    if "ticket" not in ctx.channel.name.lower():
        await ctx.send("Please create a ticket and send !bundle1 .")
        return

    user_id = ctx.author.id
    purchase_url = f"https://buy.stripe.com/28oeW999f7IccjCdQR?client_reference_id={user_id}-prod_RnrbqTAZPbJEVV"

    embed = discord.Embed(
        title="Add Credits To Key",
        description="Click the button below to complete your purchase of Bundle 1!",
        color=0x00ff00
    )
    
    embed.add_field(name="IMPORTANT:", value="You must enter your **Maelstorm Key** during checkout. If you do not already have a key, send **!getkey** to receive one.", inline=False)
    embed.add_field(name="What to do after topping up?", value=f"Download Maelstorm Bypass if you haven't already and validate it using your key. Under the usage section, you should see your current credit balance.", inline=False)

    view = discord.ui.View()
    button = discord.ui.Button(label="Buy Now", style=discord.ButtonStyle.link, url=purchase_url)
    view.add_item(button)

    await ctx.send(embed=embed, view=view)


@bot.command(name="bundle2")
async def purchase(ctx):
    if "ticket" not in ctx.channel.name.lower():
        await ctx.send("Please create a ticket and send !bundle2 .")
        return

    user_id = ctx.author.id
    purchase_url = f"https://buy.stripe.com/eVaeW9bhn7Icbfy146?client_reference_id={user_id}-prod_RnrbfKeqc7ZQN4"

    

    embed = discord.Embed(
        title="Add Credits To Key",
        description="Click the button below to complete your purchase of Bundle 2!",
        color=0x00ff00
    )
    
    embed.add_field(name="IMPORTANT:", value="You must enter your **Maelstorm Key** during checkout. If you do not already have a key, send **!getkey** to receive one.", inline=False)
    embed.add_field(name="What to do after topping up?", value=f"Download Maelstorm Bypass if you haven't already and validate it using your key. Under the usage section, you should see your current credit balance.", inline=False)

    view = discord.ui.View()
    button = discord.ui.Button(label="Buy Now", style=discord.ButtonStyle.link, url=purchase_url)
    view.add_item(button)

    await ctx.send(embed=embed, view=view)


@bot.command(name="bundle3")
async def purchase(ctx):
    if "ticket" not in ctx.channel.name.lower():
        await ctx.send("Please create a ticket and send !bundle3 .")
        return

    user_id = ctx.author.id
    purchase_url = f"https://buy.stripe.com/aEU9BP7171jO1EY003?client_reference_id={user_id}-prod_RnrcHzg9sPaVJx"

    

    embed = discord.Embed(
        title="Add Credits To Key",
        description="Click the button below to complete your purchase of Bundle 3!",
        color=0x00ff00
    )
    
    embed.add_field(name="IMPORTANT:", value="You must enter your **Maelstorm Key** during checkout. If you do not already have a key, send **!getkey** to receive one.", inline=False)
    embed.add_field(name="What to do after topping up?", value=f"Download Maelstorm Bypass if you haven't already and validate it using your key. Under the usage section, you should see your current credit balance.", inline=False)

    view = discord.ui.View()
    button = discord.ui.Button(label="Buy Now", style=discord.ButtonStyle.link, url=purchase_url)
    view.add_item(button)

    await ctx.send(embed=embed, view=view)





@bot.command(name="getkey")
async def getkey(ctx):
    if "ticket" not in ctx.channel.name.lower():
        await ctx.send("Please create a ticket and send !topup .")
        return

    user_id = ctx.author.id
    api_url = "https://desuaio.com/maelstormGenKey"
    payload = {
        "discordUserID": str(user_id),
        "initialTopUp": "2",
    }

    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.post(api_url, json=payload) as response:
                if response.status != 200 and response.status != 2001:
                    error_text = await response.text()
                    await ctx.send(
                        f"Failed to generate key. HTTP status {response.status}.\nServer says: {error_text}"
                    )
                    return

                data = await response.json()
                if data.get("status") == 200 and "keyGenerated" in data:
                    generated_key = data["keyGenerated"]
                    embed = discord.Embed(
                        title="Maelstorm Key Generated",
                        description=f"Your generated key is: **{generated_key}**.\n\n\n**2 Free Credits** have been credited to your key as well.\nPlease use this key to top up your credits.",
                        color=0x00ff00,
                    )
                    await ctx.send(embed=embed)
                elif data.get("status") == 2001 and "keyGenerated" in data:
                    generated_key = data["keyGenerated"]
                    embed = discord.Embed(
                        title="You already have a Maelstorm Key",
                        description=f"Your key is: **{generated_key}**",
                        color=0x00ff00,
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Key generation failed, please try again later.")
        except asyncio.TimeoutError:
            await ctx.send("Error: Request timed out while contacting the key generation service.")
        except Exception as e:
            await ctx.send(f"An error occurred while generating your key: {str(e)}")


@bot.command(name="checkbal")
async def checkbal(ctx):
    if "ticket" not in ctx.channel.name.lower():
        await ctx.send("Please create a ticket and send !topup .")
        return
        
    user_id = ctx.author.id
    api_url = "https://desuaio.com/maelstormCheckBalance"
    payload = {
        "discordUserID": str(user_id)
    }
    timeout = aiohttp.ClientTimeout(total=30)

    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.post(api_url, json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    await ctx.send(f"Failed to check balance. HTTP status {response.status}.\nServer says: {error_text}")
                    return
                
                data = await response.json()
                if data.get("status") == 200 and "creditBalance" in data:
                    credit = data["creditBalance"]
                    embed = discord.Embed(
                        title="Your Credit Balance",
                        description=f"Your current credit balance is: **{credit}**",
                        color=0x00ff00
                    )
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Failed to retrieve credit balance. Please try again later.")
        except asyncio.TimeoutError:
            await ctx.send("Error: Request timed out while contacting the balance service.")
        except Exception as e:
            await ctx.send(f"An error occurred while checking your balance: {str(e)}")

bot.run("MTM0MDI0MTQ3NjQzNjYyNzUxOA.G22QJQ.1ygG8WlsDIDprCT0mG3rxZgnHDD0DiJ1Q9MQkY")