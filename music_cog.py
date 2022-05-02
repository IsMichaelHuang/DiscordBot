# music_cog.py
import discord
from discord.ext import commands
import asyncio
import yt_dlp

class Music(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.voice_clients = {}
		self.ytdl = yt_dlp.YoutubeDL({
			"format": "bestaudio/best", 
			"noplaylist": True, 
			"quiet": True, 
			"extract_flat": False, 
			"skip_download": True, 
			"nocheckcertificate": True, 
			"default_search": "ytsearch1", 
			"source_address": "0.0.0.0"
		})
		self.ffmpeg_options = {
			'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
			'options': '-vn'
		}
 

	@commands.command()
	async def play(self, ctx, url):
			try:
					voice_client = await ctx.author.voice.channel.connect()
					self.voice_clients[ctx.guild.id] = voice_client
			except Exception as e:
					print(f"[play] connect error: {e}")

			try:
					loop = asyncio.get_event_loop()
					data = await loop.run_in_executor(None, lambda: self.ytdl.extract_info(url, download=False))
					song = data['url']
					player = await discord.FFmpegOpusAudio.from_probe(song, **self.ffmpeg_options)

					self.voice_clients[ctx.guild.id].play(player)
			except Exception as e:
					print(f"[play] playback error: {e}")

	@commands.command()
	async def pause(self, ctx):
			try:
					self.voice_clients[ctx.guild.id].pause()
			except Exception as e:
					print(f"[pause] error: {e}")

	@commands.command()
	async def resume(self, ctx):
			try:
					self.voice_clients[ctx.guild.id].resume()
			except Exception as e:
					print(f"[resume] error: {e}")

	@commands.command()
	async def stop(self, ctx):
			try:
					self.voice_clients[ctx.guild.id].stop()
					await self.voice_clients[ctx.guild.id].disconnect()
			except Exception as e:
					print(f"[stop] error: {e}")


