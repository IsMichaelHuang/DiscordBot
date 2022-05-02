# main.py

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from music_cog import Music

from bot_commands import (
    handle_ping, handle_clear, handle_kick, handle_ban, handle_unban,
    handle_disconnect, handle_move, handle_addrole, handle_removerole,
    handle_shutdown
)

from event_handlers import (
    on_ready_handler,
    on_command_error_handler
)

# Load .env file for DISCORD_TOKEN
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Required for command processing in latest versions

# Create bot instance
bot = commands.Bot(command_prefix='$', intents=intents)

# --- Register Events ---

@bot.event
async def on_ready():
    await on_ready_handler(bot)

@bot.event
async def on_command_error(ctx, error):
    await on_command_error_handler(ctx, error)

# --- Register Commands ---

@bot.command()
async def ping(ctx):
    await handle_ping(ctx, bot)

@bot.command()
@commands.check_any(commands.is_owner(), commands.has_role("Bot Boi"))
async def clear(ctx, amount: int = 5):
    await handle_clear(ctx, amount)

@bot.command()
@commands.check_any(commands.is_owner(), commands.has_role("Bot Boi"))
async def kick(ctx, member: discord.Member, *, reason=None):
    await handle_kick(ctx, member, reason)

@bot.command()
@commands.check_any(commands.is_owner(), commands.has_role("Bot Boi"))
async def ban(ctx, member: discord.Member, *, reason=None):
    await handle_ban(ctx, member, reason)

@bot.command()
@commands.check_any(commands.is_owner(), commands.has_role("Bot Boi"))
async def unban(ctx, *, member):
    await handle_unban(ctx, member)

@bot.command(name="disconnect", aliases=["dc"])
@commands.check_any(commands.is_owner(), commands.has_role("Bot Boi"))
async def disconnect(ctx, value: int = 10, *members: discord.Member):
    await handle_disconnect(ctx, value, members)

@bot.command()
@commands.is_owner()
async def move(ctx, member: discord.Member, channel1: discord.VoiceChannel, channel2: discord.VoiceChannel, value: int=10):
    await handle_move(ctx, member, channel1, channel2, value)

@bot.command()
@commands.check_any(commands.is_owner(), commands.has_role("Bot Boi"))
async def addrole(ctx, role: discord.Role, user: discord.Member):
    await handle_addrole(ctx, role, user)

@bot.command()
@commands.check_any(commands.is_owner(), commands.has_role("Bot Boi"))
async def remove(ctx, user: discord.Member, role: discord.Role):
    await handle_removerole(ctx, role, user)

@bot.command()
@commands.check_any(commands.is_owner(), commands.has_role("Bot Boi"))
async def shutdown(ctx):
    await handle_shutdown(ctx, bot)

async def setup():
	await bot.add_cog(Music(bot))

# Run the bot
if __name__ == "__main__":
	import asyncio

	asyncio.run(setup())
	bot.run(TOKEN)

