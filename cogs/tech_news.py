import discord
from discord.ext import commands, tasks
import feedparser

class TechNews(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.feed_urls = [
            "https://tech.hindustantimes.com/rss/tech/news",
            "https://techcrunch.com/feed/",
            "https://timesofindia.indiatimes.com/rssfeeds/66949542.cms",
        ]  # List of RSS feed URLs
        self.channel_id = 1101810840581177346  # Replace with your Discord channel ID
        self.posted_news_ids = set()  # Set to store IDs of posted news items
        self.check_news.start()

    def cog_unload(self):
        self.check_news.cancel()

    async def post_news_to_channel(self, news_item):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await channel.send(
                "**Title:** " + news_item.title + "\n" + "**Link :** " + news_item.link
            )
            # Add the ID of the posted news item to the set
            self.posted_news_ids.add(news_item.id)

    @tasks.loop(hours=1)  # Adjust the interval as per your preference
    async def check_news(self):
        for feed_url in self.feed_urls:
            feed = feedparser.parse(feed_url)
            latest_news = feed.entries[0]  # Assuming the latest entry is the first one

            # Check if the ID of the latest news item is in the set of posted news IDs
            if latest_news.id not in self.posted_news_ids:
                await self.post_news_to_channel(latest_news)

async def setup(bot):
    await bot.add_cog(TechNews(bot))