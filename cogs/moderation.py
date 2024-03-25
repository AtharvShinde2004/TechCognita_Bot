import discord
from discord.ext import commands


class Moderation(commands.Cog, name="mod"):
	def __init__(self, client):
		self.client = client
	
	
	@commands.command()
	@commands.has_permissions(ban_members=True)
	async def ban(self, ctx, member: discord.Member, * ,Reason=None):
		if ctx.author.top_role <= member.top_role and member != ctx.guild.owner:
			return await ctx.send("you can't do that")
		await ctx.guild.ban(member)
		await ctx.send(f"{member} has been banned \n**Reason**:{Reason}")
	
	
	@commands.command()
	@commands.has_permissions(manage_messages=True)
	async def clear(self, ctx, amount:int):
		await ctx.message.delete()
		await ctx.channel.purge(limit=amount)
		await ctx.send(f"<:okok:991640401880551434> Successfully deleted **{amount}** messages!")
	
	
	@commands.command()
	@commands.has_permissions(kick_members=True)
	async def kick(self, ctx, member: discord.Member, * ,Reason=None):
		if ctx.author.top_role <= member.top_role and member != ctx.guild.owner:
			return await ctx.send("you can't do that")
		await ctx.guild.kick(member)
		await ctx.send(f"{member} has been kicked \n**Reason**:{Reason}")
	
	
async def setup(client):
	await client.add_cog(Moderation(client))