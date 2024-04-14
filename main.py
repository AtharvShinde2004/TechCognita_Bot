
import os
import discord
from discord.ext import commands
import dotenv

dotenv.load_dotenv()
Token = os.getenv("Token")

EXTENSIONS = [
    "cogs.events",
    "cogs.tools",
    "cogs.moderation",
    "cogs.owner",
    "cogs.fun",
    "cogs.General",
    "cogs.tech_news",
    "cogs.utility",
    "cogs.Programming",
]

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!!",
            intents=discord.Intents.all(),
            strip_after_prefix=True,
            case_insensitive=True,
            help_command=None,
            owner_ids=[554213683102744576,1096379840011190272],
            status=discord.Status.dnd,
            activity=discord.Activity(
                type=discord.ActivityType.listening, name="!!help"
            ),
        )
        self.cd_mapping = commands.CooldownMapping.from_cooldown(1, 10, commands.BucketType.member)
        self.cooldown_enabled = True

    async def on_message(self, message):
         # Ensure commands are processed
        if message.author.bot:  # Ignore messages from bots
            return
        
        if message.author.id in self.owner_ids:  # Check if the message sender is one of the bot owners
            await self.process_commands(message)
            return
    
        if self.cooldown_enabled:
            bucket = self.cd_mapping.get_bucket(message)
            retry_after = bucket.update_rate_limit()
            
            if retry_after:
                await message.channel.send(f"You are on cooldown. Please wait {retry_after:.2f} seconds before running another command.")
                # print(f"Value of retry_after is : ( {retry_after} seconds)")
                return

        await self.process_commands(message) 

    async def setup_hook(self):
        for file in EXTENSIONS:
            await client.load_extension(file)
            print(file, "activated!")
        # await self.tree.sync()

    async def on_ready(self):
        print(
            f"""Logged in as: {client.user}
        ID: {client.user.id}
        Guilds: {len(client.guilds)}
        Users: {len(client.users)}"""
        )

    # async def on_command_error(self, ctx, error):
    #     if isinstance(error, commands.CheckFailure):
    #         await ctx.send("You don't have permission to use this command.")
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return  # Ignore CommandNotFound errors
        
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You don't have permission to use this command.")
            return

        # Handle other errors here
        # slack webhook for error reporting

client = MyBot()

@client.command()
async def toggle_cooldown(ctx):
    try:
        client.cooldown_enabled = not client.cooldown_enabled
        if client.cooldown_enabled:
            await ctx.send("Cooldown is now disabled.")
        else:
            await ctx.send("Cooldown is now enabled.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")
        print(f"An error occurred: {e}")
            
client.run(Token)
