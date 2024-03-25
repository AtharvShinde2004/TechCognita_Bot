import discord
import requests
from discord.ext import commands
import asyncio
# import config
from deepl import Translator
from datetime import datetime, timedelta, timezone
import pytz  # Import the pytz library for time zone handling
import dotenv
import os
import dotenv
import os

dotenv.load_dotenv()
DeepLAPI = os.getenv("DeepLAPI")
WeatherAPI = os.getenv("WeatherAPI")

class Utility(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.api_key = WeatherAPI
        self.deepL_client = Translator(auth_key=DeepLAPI)

    @commands.command(name="weather", description="Get current weather information for a location", usage="weather <location>")
    async def weather(self, ctx, location):
        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.api_key}&units=metric"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                city_name = data['name']
                weather_desc = data['weather'][0]['description'].capitalize()
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                
                embed = discord.Embed(title=f"Weather in {city_name}", color=discord.Color.blue())
                embed.add_field(name="Description", value=weather_desc, inline=False)
                embed.add_field(name="Temperature", value=f"{temp}°C", inline=True)
                embed.add_field(name="Feels Like", value=f"{feels_like}°C", inline=True)
                embed.add_field(name="Humidity", value=f"{humidity}%", inline=True)
                
                await ctx.send(embed=embed)
            else:
                await ctx.send("Failed to fetch weather information. Please try again later.")
        
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command(name="time", description="Get current time for a location", usage="time <location>")
    async def time(self, ctx, *location):
        if not location:
            await ctx.send("Please provide a location.")
            return

        location_str = "/".join(location)
        
        try:
            response = requests.get(f"http://worldtimeapi.org/api/timezone/{location_str}")
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            
            time_zone = data['timezone']
            current_time = data['datetime']
            
            embed = discord.Embed(title=f"Current Time in {time_zone}", description=current_time, color=discord.Color.green())
            await ctx.send(embed=embed)
        except requests.exceptions.RequestException as e:
            await ctx.send(f"Failed to fetch time information. Please try again later. Error: {e}")
        except KeyError:
            await ctx.send("Error: Unexpected response format from the World Time API.")
        except Exception as e:
            await ctx.send(f"An unexpected error occurred: {e}")

    @commands.command(name="calculate", description="Perform a mathematical calculation", usage="calculate <expression>",aliases=["calc"])
    async def calculate(self, ctx, *, expression):
        try:
            result = eval(expression)
            await ctx.send(f"Result: {result}")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="remind", description="Set a reminder for a specific time", usage="remind <time> [message]")
    async def remind(self, ctx, time, *, reminder):
        try:
            hours, minutes = map(int, time.split(':'))
            
            # Get the current UTC time as a timezone-aware object
            current_time_utc = datetime.now(timezone.utc)
            
            # Convert current UTC time to Asia/Kolkata time zone
            current_time_kolkata = current_time_utc.astimezone(pytz.timezone('Asia/Kolkata'))
            # print(current_time_kolkata)
            
            # Construct the reminder time in Asia/Kolkata time zone
            reminder_time_kolkata = current_time_kolkata.replace(hour=hours, minute=minutes, second=0, microsecond=0)
            # print(reminder_time_kolkata)
            
            # Calculate the time difference between Asia/Kolkata and UTC
            time_difference = current_time_kolkata - current_time_utc
            # print(time_difference)
            
            # Adjust the reminder time by adding the time difference
            reminder_time_utc = reminder_time_kolkata - time_difference
            # print(reminder_time_utc)
            # Check if the reminder time is in the future
            if reminder_time_utc > current_time_utc:
                delay = (reminder_time_utc - current_time_utc).total_seconds()
                await asyncio.sleep(delay)
                await ctx.send(f"Reminder: {reminder}")
            else:
                await ctx.send("Please provide a future time for the reminder.")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @commands.command(name="translate", description="Translate text to a specified language", usage="translate <language> [text]")
    async def translate(self, ctx, language, *, text):
        try:
            # Translate the text to the specified language
            translated_text = self.deepL_client.translate_text(text, target_lang=language)
            
            # Send the translated text as a message
            await ctx.send(f"Translated text ({language}): {translated_text}")
        except Exception as e:
            await ctx.send(f"Error: {e}")

async def setup(client):
    await client.add_cog(Utility(client))
