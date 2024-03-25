import discord
from discord.ext import commands
# import json
import openai
import requests
import random
import asyncio
import dotenv
import os

dotenv.load_dotenv()
ChatBotKey = os.getenv("ChatBotKey")
# import config as bot


class Events(commands.Cog):
	def __init__(self, client) :
		self.client = client
		self.hello_words = ["hi", "hello", "hlo", "hlw", "hui", "hey"]
		self.night_words = ["gn", "good night"]
		self.morning_words = ["gm", "good morning"]
	
	
	def starts(self, message, words):
		return any(message.content.lower().startswith(word) for word in words)
	
	
	@commands.Cog.listener("on_message")
	async def greetings(self, message):
		if message.author.bot:
			return
		
		if self.starts(message, self.hello_words):
			async with message.channel.typing():
				await asyncio.sleep(random.randint(1, 3))
			await message.reply(f"Hey `{message.author.name}`, Wassup!")
		if self.starts(message, self.night_words):
			async with message.channel.typing():
				await asyncio.sleep(random.randint(1, 3))
			await message.reply(f"Goodnight `{message.author.name}`, have sweet dreams <a:Eheart:826177389611712544>")
		if self.starts(message, self.morning_words):
			async with message.channel.typing():
				await asyncio.sleep(random.randint(1, 3))
			await message.reply(f"Good morning `{message.author.name}`, have a great day ahead <a:EsafaidDil:1046295562611335168>")
	
	
	# @commands.Cog.listener("on_message")
	# async def chat_bot(self, message):
	# 	if message.author.bot: return
	# 	if self.client.user not in message.mentions: return
	# 	owner = await self.client.fetch_user(554213683102744576)
	# 	msg = message.content.replace(self.client.user.mention, "")
	# 	headers = {
	# 	'Authorization': bot.ChatBotKey,
	# 	'Content-Type': 'application/json'}
		
	# 	response = requests.get(f"https://api.lebyy.me/api/chatbot?message={msg}&name={self.client.user.name}&user={message.author.id}", headers=headers).json()["message"]
		
	# 	if "Lebyy" in response:
	# 		response = response.replace("Lebyy", f"`Team TechCognita[{owner.name}]`")
		
	# 	async with message.channel.typing():
	# 		await asyncio.sleep(random.randint(1, 3))
	# 	await message.reply(response)

	@commands.Cog.listener("on_message")
	async def chat_bot(self, message):
		if message.author.bot:
			return
		if self.client.user not in message.mentions:
			return

		try:
			openai.api_key = ChatBotKey  # Set OpenAI API key
			response = openai.Completion.create(
				engine="text-davinci-002",
				prompt=f"{message.content}",
				max_tokens=2048,
				temperature=0.5
			)
			# response_text = response.choices[0].text.strip()
			await message.channel.send(response.choices[0].text)
		except Exception as e:
			response_text = "Sorry, I couldn't understand that right now."

		async with message.channel.typing():
			await asyncio.sleep(random.randint(1, 3))
		await message.reply(response_text)
	
	@commands.Cog.listener()
	async def on_command_error(self, ctx, error):
		if isinstance(error, commands.MissingPermissions):
			await ctx.send("You don't have enough permissions to do that")
			return
			
		embed = discord.Embed(title="Error!", description=error, color=discord.Colour.red())
		await ctx.send(embed=embed, mention_author=False)
	
	
async def setup(client):
	await client.add_cog(Events(client))