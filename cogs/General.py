import discord
from discord.ext import commands
import time


class General(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.initial_time = time.time()

    @commands.command(name="help", description="Display list of available commands")
    async def help(self, ctx, *, command=None):
        if command:
            command = self.client.get_command(command.lower())
            if not command:
                await ctx.send("Command not found.")
                return

            em = discord.Embed(color=discord.Colour.dark_theme())
            em.set_author(
                name=f"{command.name} command", icon_url=ctx.me.display_avatar.url )
            em.add_field(
                name="**Instructions**",
                value=">>> Required: `<>`\nOptional: `[]`\nDo not type this when using commands.",
                inline=False,)
            em.add_field(
                name="**Usage**", value=f"> `{ctx.prefix}{command.usage}`", inline=False)
            em.add_field(
                name="**Aliases**",
                value=f"> `{', '.join(command.aliases) or 'None'}`",
                inline=False,)
            em.add_field(
                name="**Description**", value=f"> `{command.description}`", inline=False)
            em.set_footer(text=f"Requested by {ctx.author}.")
            await ctx.send(embed=em)
        else:
            # em = discord.Embed(description = "Hey there! I am TechCognita Manager, My Prefix is `!!`,\n Thanks for adding me in your server.", color = ctx.author.color)
            # em.set_author(name = ctx.author.display_name, icon_url = ctx.author.display_avatar.url)
            # em.add_field(name = "**General Commands**", value = "`help, info, ping, serverinfo, userinfo`", inline = False)
            # em.add_field(name = "**Fun commands**", value = "`coinflip, roll, say,fact, joke, quote,`", inline = False)
            # em.add_field(name = "**Tools Commands**", value = "`avatar, membercount, embed, nick`", inline = False)
            # em.add_field(name = "**Moderation commands**", value = "`ban, clear, kick`")
            # em.add_field(name = "**Utility Commands**", value = "`weather, time, calculate, remind, translate`", inline = False)
            # em.set_footer(
            #     text="Use `!!invite` to add me in Your server",
            #     icon_url=ctx.author.display_avatar.url,
            # )
            # await ctx.send(embed=em)
            em = discord.Embed(
                description="Hey there! I am TechCognita Manager, My Prefix is `!!`,\n Thanks for adding me in your server.",
                color=ctx.author.color,
            )
            em.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url
            )

            # Iterate through command categories (cogs)
            for cog in self.client.cogs:
                cog_commands = self.client.get_cog(cog).get_commands()
                if cog_commands:
                    em.add_field(
                        name=f"**{cog}**",
                        value=", ".join([f"`{cmd.name}`" for cmd in cog_commands]),
                        inline=False,
                    )

            em.set_footer(
                text="Use `!!invite` to add me in Your server",
                icon_url=ctx.author.display_avatar.url,
            )
            await ctx.send(embed=em)

    @commands.command(name="info", description="Display information about the bot")
    async def info(self, ctx):
        embed = discord.Embed(title="Bot Information", color=discord.Color.blue())
        embed.add_field(name="Creator", value="TechCognita Team", inline=False)
        embed.add_field(name="Version", value="1.0.0", inline=False)
        embed.add_field(name="Library", value="discord.py", inline=False)
        embed.set_footer(text="TechCognita Bot - Your Discord Assistant")
        await ctx.send(embed=embed)

    @commands.command(
        name="serverinfo", description="Display information about the server"
    )
    @commands.guild_only()
    async def serverinfo(self, ctx):
        guild = ctx.guild
        format = "%a, %d %b %Y | %H:%M:%S %ZGMT"
        embed = discord.Embed(color=ctx.guild.owner.top_role.color)
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        categories = len(ctx.guild.categories)
        channels = text_channels + voice_channels
        # embed.set_thumbnail(url = str(ctx.guild.icon.url))
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        else:
            embed.set_thumbnail(
                url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUmwxVUVHKghNMUPVAEUstFVgsstYLd5hKNk-vAuQURHStOrz4jmFSTZ8UvaJSZihYccQ"
            )  # Default server icon
        embed.add_field(
            name=f"Information About **{ctx.guild.name}**: ",
            value=f":white_small_square: ID: **{ctx.guild.id}** \n:white_small_square: Owner: **{ctx.guild.owner}**\n:white_small_square: Creation: **{ctx.guild.created_at.strftime(format)}** \n:white_small_square: Members: **{ctx.guild.member_count}** \n:white_small_square: Channels: **{channels}** Channels; **{text_channels}** Text, **{voice_channels}** Voice, **{categories}** Categories \n:white_small_square: Verification: **{str(ctx.guild.verification_level).upper()}** \n:white_small_square: Features: {', '.join(f'**{x}**' for x in ctx.guild.features)} \n:white_small_square: Splash: {ctx.guild.splash}",
        )
        await ctx.send(embed=embed)

    @commands.command(name="userinfo", description="Display information about a user")
    async def userinfo(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(
            title=f"User Information - {member.name}", color=member.color
        )
        embed.set_thumbnail(url=member.avatar.url)
        embed.add_field(name="ID", value=member.id, inline=True)
        embed.add_field(name="Nickname", value=member.nick or "None", inline=True)
        embed.add_field(name="Status", value=member.status, inline=True)
        embed.add_field(
            name="Created At",
            value=member.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            inline=True,
        )
        await ctx.send(embed=embed)

    @commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, ctx):
        await ctx.message.reply(f"Pong! **{round(self.client.latency * 1000)}ms**")

    @commands.command(name="runtime", description="Returns bot's runtime.")
    async def runtime(self, ctx):
        seconds = int(time.time() - self.initial_time)
        runtime = time.strftime("%Hhr %Mmin %Ssec", time.gmtime(seconds))
        await ctx.reply(f"**{runtime}**")

    @commands.command(name="invite", description="Sends invite links.")
    async def invite(self, ctx):
        embed = discord.Embed(
            title="Invite links",
            description="[Invite me](https://discord.com/oauth2/authorize?client_id=1221066077925146675&permissions=8&scope=bot)\n\n[Support Server](https://discord.gg/57n8PkNbaP)",
            color=0xFF9900,
        )
        await ctx.send(embed=embed)


async def setup(client):
    await client.add_cog(General(client))
