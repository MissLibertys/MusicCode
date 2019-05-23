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

@bot.command()
async def ping(ctx):
  pingtime = time.time()
  pingms = await ctx.send("Pinging...")
  ping = (time.time() - pingtime) * 1000
  await ctx.edit_message(pingms, "Pong! :ping_pong: ping time is `%dms`" % ping)
  
bot.run(os.environ["BOT_TOKEN"])
