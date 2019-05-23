import discord
from discord.ext import commands
import os

bot = commands.Bot(command_prefix = "m.")

@bot.event
async def on_ready():
  print("Logged in as")
  print("User Name", bot.user.name)
  print("User ID", bot.user.id)
  
@bot.command()
async def test(ctx):
  await ctx.send("test")
  
bot.run(os.environ["BOT_TOKEN"])
