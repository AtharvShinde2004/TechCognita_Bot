import discord
from discord.ext import commands


class Owner(commands.Cog):
	def __init__(self, client):
		self.client = client

async def cog_check(self, ctx):
	return await self.bot.is_owner(ctx.author)
# Check if the command invoker is the bot owner


@commands.command()
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
	await self.bot.close()

@commands.command(name="reload", hidden=True)
async def reload(self, ctx, *, cog: str):
	"""Reload a cog."""
	try:
		self.bot.reload_extension(cog)
		await ctx.send(f"Cog `{cog}` reloaded successfully.")
	except commands.ExtensionError as e:
		await ctx.send(f"Failed to reload cog `{cog}`: {e}")


async def setup(client):
	await client.add_cog(Owner(client))