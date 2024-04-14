import discord
from discord.ext import commands


class Owner(commands.Cog):
	def __init__(self, client):
		self.client = client

	async def cog_check(self, ctx):
		return await self.client.is_owner(ctx.author)
	# Check if the command invoker is the bot owner


	@commands.command( hidden=True)
	@commands.is_owner()
	async def stats(self, ctx):
		em = discord.Embed(color=discord.Colour.random())
		em.set_author(name=ctx.me, icon_url=ctx.me.display_avatar.url)
		em.add_field(name="Ping", value=f"{round(self.client.latency * 1000)}ms", inline=False)
		em.add_field(name="Users", value=len(self.client.users), inline=False)
		em.add_field(name="Guilds", value=len(self.client.guilds), inline=False)
		await ctx.send(embed=em)



	@commands.command(name="shutdown", hidden=True)
	async def shutdown(self, ctx):
		"""Shut down the bot."""
		await ctx.send("Shutting down...")
		await ctx.send("Guys me ja rha hu byyy..............")
		await self.client.logout()
		# await self.client.close()  
    
		# close() is an immediate shutdown of the bot, while logout() initiates a graceful logout process where the bot remains active until it receives confirmation from Discord.

	@commands.command(name="reload", hidden=True)
	async def reload(self, ctx, *, cog: str = None):
		"""Reload a cog."""
		if cog is None:
			await ctx.send("Please specify a cog to reload or 'all' to reload all cogs.")
			return

		if cog.lower() == "all":
			for extension in self.client.extensions:
				try:
					await self.client.reload_extension(extension)
					await ctx.send(f"Cog `{extension}` reloaded successfully.")
				except commands.ExtensionError as e:
					await ctx.send(f"Failed to reload cog `{extension}`: {e}")
		else:
			try:
				# await self.client.reload_extension(cog)
				await self.client.reload_extension(f"cogs.{cog}")
				await ctx.send(f"Cog `{cog}` reloaded successfully.")
			except commands.ExtensionError as e:
				await ctx.send(f"Failed to reload cog `{cog}`: {e}")
	
	@commands.command(name="leave", hidden=True)
	@commands.is_owner()
	async def leave(self, ctx, *, server_id: int):
		"""Command to make the bot leave a server."""
		try:
			guild = self.client.get_guild(server_id)
			if guild:
				await guild.leave()
				await ctx.send(f"Left server: {guild.name}")
			else:
				await ctx.send("Server not found or bot is not in that server.")
		except Exception as e:
			await ctx.send(f"Failed to leave server: {e}")

	# @commands.command(name="serverlist", hidden=True)
	# async def server_list(self, ctx):
	# 	"""Command to list all servers the bot is currently in."""
	# 	servers = [guild.name for guild in self.client.guilds]
	# 	servers_list = "\n".join(servers)
	# 	embed = discord.Embed(title="Server List", description=servers_list, color=discord.Color.blue())
	# 	await ctx.send(embed=embed)

	@commands.command(name="serverlist", hidden=True)
	@commands.is_owner()
	async def server_list(self, ctx):
		"""Command to list all servers the bot is currently in."""
		embed = discord.Embed(title="Server List", color=discord.Color.blue())
		for guild in self.client.guilds:
			try:
				invite = await guild.text_channels[0].create_invite(max_age=86400, max_uses=1, unique=True)
				embed.add_field(name=f"{guild.name} (ID: {guild.id})", value=f"Invite Link: {invite}", inline=False)
			except Exception as e:
				embed.add_field(name=f"{guild.name} (ID: {guild.id})", value=f"Failed to generate invite link: {e}", inline=False)
		await ctx.send(embed=embed)

async def setup(client):
	await client.add_cog(Owner(client))