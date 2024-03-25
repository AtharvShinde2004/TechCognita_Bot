import discord
from discord.ext import commands
import json
import requests
import random

class Fun(commands.Cog):
	def __init__(self, client):
		self.client = client
	
	
	@commands.command(name="coinflip", description="Flips a coin.", aliases=["cf"], usage="!!cf [Heads or Tails] or !!coinflip [Heads or Tails]")
	async def coinflip(self, ctx):
		outcomes = ["Heads!", "Tails!"]
		result = random.choice(outcomes)
		await ctx.reply(f'The Coin spins.. and its **{result}**')
	
	
	@commands.command(name="roll", description="Rolls a dice.",  usage="!!roll [number]")
	async def roll(self, ctx, end: int=100):
		await ctx.send(f"{ctx.author.mention} Rolled: **{random.randint(1, end)}** (1-{end})")
	
	
	@commands.command(name="say", description="Repeats a message.", aliases=["repeat", "echo"], usage="!!say <message>")
	async def say(self, ctx, *, message):
		await ctx.message.delete()
		await ctx.send(message)
	
	@commands.command(name="fact", description="Sends a random fact", usage="!!fact")
	async def fact(self, ctx):
		url = 'https://useless-facts.sameerkumar.website/api'
		response = requests.get(url)
		data = json.loads(response.text)
		fact = data['data']
		embed = discord.Embed(title="Fact", description=f"{fact}", color=discord.Colour.random())
		embed.set_footer(text=f"Information requested by: {ctx.author}")
		await ctx.send(embed=embed)

	@commands.command(name="joke", description="Tells a random joke", usage="!!joke")
	async def joke(self, ctx):
		url = 'https://official-joke-api.appspot.com/random_joke'
		response = requests.get(url)
		data = json.loads(response.text)
		setup = data['setup']
		punchline = data['punchline']
		embed = discord.Embed(title="Joke", description=f"{setup}\n\n{punchline}", color=discord.Colour.random())
		embed.set_footer(text=f"Information requested by: {ctx.author}")
		await ctx.send(embed=embed)

	@commands.command(name="quote", description="Sends a random quote", usage="!!qoute")
	async def quote(self, ctx):
		url = 'https://api.quotable.io/random'
		response = requests.get(url)
		data = response.json()
		author = data['author']
		content = data['content']
		embed = discord.Embed(title="Quote", description=f"{content} \n  ", color=discord.Colour.random())
		embed.add_field(name="", value="", inline=True)
		embed.add_field(name=f'- {author}', value="", inline=True)
		embed.set_footer(text=f"Information requested by: {ctx.author}")
		await ctx.send(embed=embed)
	
async def setup(client):
	await client.add_cog(Fun(client))