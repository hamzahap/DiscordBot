import os
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Set command prefix for bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello, world!')

@bot.command()
async def addrole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f"{user.mention} has been given the {role.name} role.")

@bot.command()
async def removerole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f"{role.name} has been removed from {user.mention}.")

@bot.command()
async def timeout(ctx, user: discord.Member, duration: int):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")  # assuming you have a role named "Muted"
    if not muted_role:
        # If the Muted role doesn't exist, create it
        muted_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(muted_role, send_messages=False)
    
    await user.add_roles(muted_role)
    await ctx.send(f"{user.mention} has been muted for {duration} seconds.")
    await asyncio.sleep(duration)
    await user.remove_roles(muted_role)

@bot.command()
async def canceltimeout(ctx, user: discord.Member):
    muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if muted_role in user.roles:
        await user.remove_roles(muted_role)
        await ctx.send(f"{user.mention}'s timeout has been cancelled.")
    else:
        await ctx.send(f"{user.mention} is not in timeout.")

@bot.command()
async def mute(ctx, user: discord.Member):
    await user.edit(mute=True)
    await ctx.send(f"{user.mention} has been muted.")

@bot.command()
async def unmute(ctx, user: discord.Member):
    await user.edit(mute=False)
    await ctx.send(f"{user.mention} has been unmuted.")

bot.run(TOKEN)
