import discord
from discord.ext import commands
import aiohttp
import asyncio
import cv2
import numpy as np
import random
import string
import io

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)



def generate_captcha():
    # Generate a random 5-character captcha (letters and digits)
    captcha_text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
    
    # Create a white image
    width, height = 200, 100
    image = np.ones((height, width, 3), dtype=np.uint8) * 255
    
    # Draw the text (centered) on the image
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1.5
    thickness = 3
    text_size, _ = cv2.getTextSize(captcha_text, font, font_scale, thickness)
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 2
    cv2.putText(image, captcha_text, (text_x, text_y), font, font_scale, (0, 0, 0), thickness, cv2.LINE_AA)
    
    # Optionally, add some random lines for complexity
    for _ in range(8):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        cv2.line(image, (x1, y1), (x2, y2), (0, 0, 0), 1)
    
    # Save the image to an in-memory file
    _, buffer = cv2.imencode('.png', image)
    io_buf = io.BytesIO(buffer)
    file = discord.File(fp=io_buf, filename="captcha.png")
    
    return captcha_text, file

@bot.event
async def on_member_join(member):
    if member.bot:
        return
    try:
        dm_channel = await member.create_dm()
        await dm_channel.send("Welcome to the server! Please complete the verification below by solving the captcha.")
        captcha_text, captcha_file = generate_captcha()
        await dm_channel.send("Please type the text shown in the image below:", file=captcha_file)

        def check(m):
            return m.author == member and m.channel == dm_channel
        response = await bot.wait_for("message", check=check, timeout=60.0)

        if response.content.strip() == captcha_text:
            await dm_channel.send("Verification successful! You now have access to the server.")
            role = member.guild.get_role(1342095270904594534)
            if role:
                await member.add_roles(role)
            else:
                await dm_channel.send("Verification passed, but the role was not found.")
        else:
            await dm_channel.send("Incorrect captcha. Please retrigger verification by sending \"!verify\".")
    except asyncio.TimeoutError:
        await dm_channel.send("You took too long to respond. You can retrigger verification by sending \"!verify\".")

@bot.command(name="verify")
async def verify(ctx):
    # Ensure the command is run in DMs.
    if ctx.guild is not None:
        try:
            await ctx.author.send("For security, please use the !verify command in DMs.")
        except Exception:
            await ctx.send("Please use the !verify command in DMs.")
        return

    member = ctx.author

    guild = next((g for g in bot.guilds if g.get_member(member.id)), None)
    if guild is None:
        await ctx.send("Could not find a guild where you are a member.")
        return

    role = guild.get_role(1342095270904594534)
    guild_member = guild.get_member(member.id)
    if role in guild_member.roles:
        await ctx.send("You already have the designated role. No need to verify again!")
        return

    try:
        captcha_text, captcha_file = generate_captcha()
        await ctx.send("Please type the text shown in the image below:", file=captcha_file)

        def check(m):
            return m.author == member and m.channel == ctx.channel

        response = await bot.wait_for("message", check=check, timeout=60.0)

        if response.content.strip() == captcha_text:
            await ctx.send("Verification successful! You now have access to the server.")
            try:
                await guild_member.add_roles(role)
                await ctx.send("Role assigned successfully!")
            except Exception as e:
                await ctx.send("An error occurred while assigning your role.")
        else:
            await ctx.send("Incorrect captcha. Please try again by sending \"!verify\".")
    except asyncio.TimeoutError:
        await ctx.send("Verification timed out. Please try again by sending \"!verify\".")




# @bot.command(name="admintest")
# @commands.has_permissions(administrator=True)
# async def admintest(ctx):
#     role = ctx.guild.get_role(1342095270904594534)
#     if role is None:
#         return await ctx.send("Error: Role not found in this server.")

#     online_members = [member for member in ctx.guild.members
#                       if not member.bot and member.status != discord.Status.offline]

#     if not online_members:
#         return await ctx.send("No online members found. Make sure Presences Intent is enabled in your developer portal and in your code.")

#     count_assigned = 0
#     for member in online_members:
#         try:
#             print(f"Adding {count_assigned}")
#             await member.add_roles(role)
#             count_assigned += 1
#         except Exception as e:
#             print(f"Error assigning role to {member}: {e}")

#     await ctx.send(f"Assigned the role to {count_assigned} online members.")




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

bot.run("")



# https://discord.gg/r9umYM9qc5