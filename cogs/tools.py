import discord
from discord.ext import commands
import datetime

class Tools(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	@commands.command(name="avatar", description="Displays a user avatar.", aliases=["av", "pfp"], usage="!!av or !!pfp")
	async def avatar(self, ctx, member: discord.Member=commands.Author):
		embed = discord.Embed(title = 'Avatar')
		embed.set_author(name = member, icon_url = member.display_avatar.url)
		embed.set_image(url = member.display_avatar.url)
		embed.set_footer(text=f'Requested by: {ctx.author.name}',icon_url = ctx.author.display_avatar.url)
		await ctx.send(embed=embed)
		

	@commands.command(name="Members_count", description="Displays a Members Count.", aliases=["mc", "members", "memberscount"], usage="!!mc or !!members or !!memberscount")
	async def membercount(self, ctx):
		memb = ctx.guild.member_count 

		em = discord.Embed(
			title="Members",
			description=f"{ctx.guild.member_count}",
			color=ctx.author.color,
			timestamp=datetime.datetime.now(datetime.timezone.utc),
		)
		await ctx.send(embed=em)
	
	
	@commands.command(name="embed", description="Sends an embed.", aliases=["em"], usage="!!em")
	async def embed(self, ctx, *, text):
		embed = discord.Embed(title = text, color = ctx.author.color)
		await ctx.send(embed=embed)
	
	
	@commands.command(name="nickname", description="Change nickname of a member.",aliases = ["setnick","nick"], usage="!!nick or !!setnick")
	@commands.has_permissions(manage_nicknames=True)
	async def nickname(self, ctx, member:discord.Member, *, nick = None):
		try:
			await member.edit(nick=nick)
			await ctx.send("Nickname was changed")
		except:
			await ctx.send("Unable to change nickname")
	
	
async def setup(client):
	await client.add_cog(Tools(client))