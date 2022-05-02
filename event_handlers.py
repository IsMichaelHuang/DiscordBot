# event_handlers.py
import discord
from discord.ext import commands

async def on_ready_handler(bot):
    await bot.change_presence(status=discord.Status.invisible)
    print("The Bot is ready.")

async def on_command_error_handler(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Not a command in here.")
    else:
        print(f"Error: {error}")


