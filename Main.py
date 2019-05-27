import discord
from discord.ext import commands
import os
import time
import youtube_dl
import inspect
import requests, bs4
from discord import opus

bot = commands.Bot(command_prefix = "m.")
bot.remove_command("help")

players = {}

@bot.event
async def on_ready():
  print("Logged in as")
  print("User Name", bot.user.name)
  print("User ID", bot.user.id)

@bot.command()
async def ping():
  await bot.say("Pong! :ping_pong: ping time is `116ms`")
  
@bot.command(pass_context=True, no_pm=True)
async def join(ctx):
	user = ctx.message.author
	channel = ctx.message.author.voice.voice_channel
	await bot.join_voice_channel(channel)
	embed = discord.Embed(colour=user.colour)
	embed.add_field(name="Successfully connected to voice channel:", value=channel)
	await bot.say(embed=embed)
	
@bot.command(pass_context=True, no_pm=True)
async def leave(ctx):
	user = ctx.message.author
	server = ctx.message.server
	channel = ctx.message.author.voice.voice_channel
	voice_client = bot.voice_client_in(server)
	await voice_client.disconnect()
	embed = discord.Embed(colour=user.colour)
	embed.add_field(name="Successfully disconnected from:", value=channel)
	await bot.say(embed=embed)

@bot.command(pass_context=True)
async def pause(ctx):
	user = ctx.message.author
	id = ctx.message.server.id
	players[id].pause()
	embed = discord.Embed(colour=user.colour)
	embed.add_field(name="Player Paused", value=f"Requested by {ctx.message.author.name}")
	await bot.say(embed=embed)

@bot.command(pass_context=True)
async def skip(ctx):
	user = ctx.message.author
	id = ctx.message.server.id
	players[id].stop()
	embed = discord.Embed(colour=user.colour)
	embed.add_field(name="Player Skipped", value=f"Requested by {ctx.message.author.name}")
	await bot.say(embed=embed)
	
@bot.command(pass_context=True)
async def play(ctx, *, name):
	author = ctx.message.author
	name = ctx.message.content.replace("m.play ", '')
	fullcontent = ('http://www.youtube.com/results?search_query=' + name)
	text = requests.get(fullcontent).text
	soup = bs4.BeautifulSoup(text, 'html.parser')
	img = soup.find_all('img')
	div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
	a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
	title = (a[0]['title'])
	a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
	url = ('http://www.youtube.com'+a0['href'])
	server = ctx.message.server
	voice_client = bot.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
	players[server.id] = player
	print("User: {} From Server: {} is playing {}".format(author, server, title))
	player.start()
	embed = discord.Embed(description=" ")
	embed.add_field(name="Now Playing", value=title)
	await bot.say(embed=embed)
	
@bot.command(pass_context=True)
async def queue(ctx, *, name):
	name = ctx.message.content.replace("m.queue ", '')
	fullcontent = ('http://www.youtube.com/results?search_query=' + name)
	text = requests.get(fullcontent).text
	soup = bs4.BeautifulSoup(text, 'html.parser')
	img = soup.find_all('img')
	div = [ d for d in soup.find_all('div') if d.has_attr('class') and 'yt-lockup-dismissable' in d['class']]
	a = [ x for x in div[0].find_all('a') if x.has_attr('title') ]
	title = (a[0]['title'])
	a0 = [ x for x in div[0].find_all('a') if x.has_attr('title') ][0]
	url = ('http://www.youtube.com'+a0['href'])
	server = ctx.message.server
	voice_client = bot.voice_client_in(server)
	player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
	
	if server.id in queues:
		queues[server.id].append(player)
	else:
		queues[server.id] = [player]
	embed = discord.Embed(description=" ")
	embed.add_field(name="Video queued", value=title)
	await bot.say(embed=embed)

@bot.command(pass_context=True)
async def resume(ctx):
	user = ctx.message.author
	id = ctx.message.server.id
	players[id].resume()
	embed = discord.Embed(colour=user.colour)
	embed.add_field(name="Player Resumed", value=f"Requested by {ctx.message.author.name}")
	await bot.say(embed=embed)
	
@bot.command(pass_context=True, name="stats")
async def _stats(ctx):
	servers = list(client.servers)
	current_time = time.time()
	difference = int(round(current_time - start_time))
	text = str(datetime.timedelta(seconds=difference))
	embed = discord.Embed(title="Servers:", description=f"{str(len(servers))}", color=0xFFFF)
	embed.add_field(name="Users:", value=f"{str(len(set(client.get_all_members())))}")
	embed.add_field(name="Uptime:", value=f"{text}")
	await bot.say(embed=embed)
	
@bot.command(pass_context=True)
async def support(ctx):
	user = ctx.message.author
	embed = discord.Embed(color=user.colour)
	embed.add_field(name="Support server", value=f"[Link](https://discord.gg/ccAuKgV)")
	embed.set_thumbnail(url="https://cdn.discordapp.com/avatars/489033991769423873/5215f2354e333ef5ca21124d45f70efd.png?size=1024")
	await bot.say(embed=embed)
	
@bot.command(pass_context=True)
async def invite(ctx):
	user = ctx.message.author
	embed = discord.Embed(color=user.colour)
	embed.add_field(name="Bot Link", value=f"[Link](https://discordapp.com/api/oauth2/authorize?client_id=489033991769423873&permissions=36785152&redirect_uri=https%3A%2F%2Fdiscordapp.com%2Foauth2%2Fauthorize%3Fclient_id%3D489033991769423873%26permissions%3D36784128%26redirect_uri%3Dhttps%253A%252F%252Fdiscordapp.com%252Fapi%252Foauth2%252Fauthorize%253Fclient_id&scope=bot)")
	await bot.say(embed=embed)
	
@bot.command(pass_context=True)
async def help(ctx):
	user = ctx.message.author
	embed = discord.Embed(colour=user.colour)
	embed.add_field(name="Music commands:", value="m.play | m.join | m.leave | m.pause | m.resume | m.skip | m.queue", inline=True)
	embed.add_field(name="Credits:", value="m.credits")
	embed.add_field(name="Other commands:", value="m.ping | m.support | m.stats | m.invite")
	await bot.say(embed=embed)

@bot.command(no_pm=True)
async def credits(ctx):
	"""credits who helped me"""
	await bot.say('iHoverZz#2321 helped me with this music bot')
	
def user_is_me(ctx):
	return ctx.message.author.id == "277983178914922497"

@bot.command(name='eval')
@commands.check(user_is_me)
async def _eval(ctx, *, command):
	res = eval(command)
	if inspect.isawaitable(res):
		await bot.say(await res)
	else:
		await bot.delete_message(ctx.message)
		await bot.say(res)
        
@_eval.error
async def eval_error(error, ctx):
	if isinstance(error, discord.ext.commands.errors.CheckFailure):
		text = "Sorry {}, You can't use this command only the bot owner can do this.".format(ctx.message.author.mention)
		await bot.say(ctx.message.channel, text)
  
bot.run(os.environ["BOT_TOKEN"])
