import discord
from discord.ext import commands
import requests
import dotenv
import os
dotenv.load_dotenv()
Youtube = os.getenv("YoutubeApi")
class Programming(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(name="code", description="Run code in a specified programming language")
    async def code(self, ctx, language, *, code):
        # Implement code execution logic here using Rextester API
        response = requests.post("https://rextester.com/rundotnet/api", data={"LanguageChoice": language, "Program": code})
        output = response.json().get("Result", "No output")
        await ctx.send(f"Running {language} code: \n```{output}```")

    @commands.command(name="learn", description="Get resources to learn about a programming topic")
    async def learn(self, ctx,*, topic):
        # Make a request to the YouTube Data API's search endpoint
        params = {
            "q": topic,
            "part": "snippet",
            "maxResults": 10,
            "key": Youtube
        }
        response = requests.get("https://www.googleapis.com/youtube/v3/search", params=params)
        
        # Parse the response and extract relevant information
        data = response.json().get("items", [])
        if data:
            video = data[0]
            video_id = video.get("id", {}).get("videoId")
            if video_id:
                title = video["snippet"]["title"]
                description = video["snippet"]["description"]
                thumbnail_url = video["snippet"]["thumbnails"]["default"]["url"]
                link = f"https://www.youtube.com/watch?v={video_id}"
                
                # Display the extracted information in the bot's response
                embed = discord.Embed(title=title, description=description, url=link)
                embed.set_thumbnail(url=thumbnail_url)
                await ctx.send(embed=embed)
            else:
                await ctx.send("No learning resources found on YouTube.")
        else:
            await ctx.send("No learning resources found on YouTube.")

    @commands.command(name="stackoverflow", description="Search Stack Overflow for programming solutions")
    async def stackoverflow(self, ctx, query):
        # Implement Stack Overflow search logic here using Stack Exchange API
        response = requests.get("https://api.stackexchange.com/2.3/search", params={"intitle": query, "site": "stackoverflow"})
        items = response.json().get("items", [])
        if items:
            question = items[0]
            title = question["title"]
            link = question["link"]
            await ctx.send(f"Top Stack Overflow result for '{query}': [{title}]({link})")
        else:
            await ctx.send("No results found on Stack Overflow.")

    @commands.command(name="github", description="Get information about a GitHub repository")
    async def github(self, ctx, repo):
        # Implement GitHub repository information retrieval logic here using GitHub API
        response = requests.get(f"https://api.github.com/repos/{repo}")
        if response.status_code == 200:
            repo_info = response.json()
            name = repo_info["full_name"]
            description = repo_info["description"]
            stars = repo_info["stargazers_count"]
            forks = repo_info["forks_count"]
            await ctx.send(f"Repository: {name}\nDescription: {description}\nStars: {stars}\nForks: {forks}")
        else:
            await ctx.send("Repository not found.")

async def setup(client):
    await client.add_cog(Programming(client))
