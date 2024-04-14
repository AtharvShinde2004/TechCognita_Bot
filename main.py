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


    async def setup_hook(self):
        for file in EXTENSIONS:
            await self.load_extension(file)
            print(file, "activated!")
        await self.tree.sync()


    async def on_ready(self):
        print(
            f"""Logged in as: {self.user}
        ID: {self.user.id}
        Guilds: {len(self.guilds)}
        Users: {len(self.users)}"""
        )


    async def on_command_error(self, ctx, error):
            if isinstance(error, commands.CheckFailure):
                await ctx.send("You don't have permission to use this command.")


client = MyBot()
client.run(Token)
