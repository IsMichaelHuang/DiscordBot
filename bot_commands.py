# bot_commands.py
import asyncio
import random
import discord

# Ping
async def handle_ping(ctx, bot):
    await ctx.send(f'Ping! {round(bot.latency * 1000)}ms')

# Clear Messages
async def handle_clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount)

# Kick Member
async def handle_kick(ctx, member: discord.Member, reason=None):
    if str(member.id) == "193219019292016641":
        print(member, " tried to kick you")
        return

    await ctx.channel.purge(limit=1)
    print("Kick member:", member)
    await member.kick(reason=reason)

# Ban Member
async def handle_ban(ctx, member: discord.Member, reason=None):
    if str(member.id) == "193219019292016641":
        print(member, " tried to ban you")
        return

    await ctx.channel.purge(limit=1)
    print("Ban member:", member)
    await member.ban(reason=reason)

# Unban Member
async def handle_unban(ctx, member_str):
    await ctx.channel.purge(limit=1)

    banned_users = await ctx.guild.bans()
    name, discriminator = member_str.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (name, discriminator):
            await ctx.guild.unban(user)
            print(f"Unbanned member: {user}")
            return

# Disconnect Members (loop)
async def handle_disconnect(ctx, value: int, members: list):
    await ctx.channel.purge(limit=1)
    for member in members:
        print("log:", member, " Iteration:", value)

        if str(member.id) == "193219019292016641":
            print(member, " tried to DC you.")
            return

        for _ in range(value):
            delay = random.randint(1, 3)
            await asyncio.sleep(delay)
            await member.move_to(None)

        print("Event over for", member)

# Move Member Between Two Channels
async def handle_move(ctx, member: discord.Member, ch1: discord.VoiceChannel, ch2: discord.VoiceChannel, value=10):
    await ctx.channel.purge(limit=1)

    print(f"Moving {member} between {ch1} and {ch2}")
    for i in range(value):
        channel = ch1 if i % 2 == 0 else ch2
        await member.move_to(channel)
        await asyncio.sleep(0.4)

# Add Role
async def handle_addrole(ctx, role: discord.Role, user: discord.Member):
    await ctx.channel.purge(limit=1)
    await user.add_roles(role)

# Remove Role
async def handle_removerole(ctx, role: discord.Role, user: discord.Member):
    await ctx.channel.purge(limit=1)
    await user.remove_roles(role)

# Shutdown
async def handle_shutdown(ctx, bot):
    await ctx.send("Shutting Down...")
    await asyncio.sleep(2)
    await ctx.channel.purge(limit=2)
    await bot.close()
