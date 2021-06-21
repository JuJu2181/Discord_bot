#connecting a bot to a channel
#Bot is a subclass of Client with added functions

import os
import random
import discord
from dotenv import load_dotenv
from datetime import datetime, date
import time
import pytz
import youtube_dl
import asyncio
import praw
import threading

import joke_api
import quotes_api
import check_ping
import weather_api
import reddit_file
#import memes_api

#1
from discord.ext import commands, tasks
from random import choice
#from bot_life import keep_alive

#keep_alive()

#Youtube DL#
youtube_dl.utils.bug_reports_message = lambda: ''
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0', # bind to ipv4 since ipv6 addresses cause issues sometimes
    'forceduration': True 
}

ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
#to get duration of yt video
# dictmeta = ytdl.extract_info("https://www.youtube.com/watch?v=FSUHeqhVvpc")
# print(dictmeta['duration'])

videoDuration = 0
class YTDLSource(discord.PCMVolumeTransformer):
    
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        global videoDuration
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        videoDuration = data['duration']
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

#print(videoDuration)
## load env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
REDDIT_APP_ID = 'ev455l_XxV7R5g'
REDDIT_APP_SECRET = 's9Tz42N_AAPe0I0zawhSR7Mbio3TQQ'
REDDIT_MEME = ['funny','meme','wtf']
#GUILD = os.getenv('DISCORD_GUILD')

#TOKEN = 'NzMyOTgxMzAzMTYyNDM3NzMz.XxVpYQ.SanIqXTlntglEgRG0_vtauLXG58'
#GUILD = 'Python_App_Tests'

#2
#client = discord.Client()
bot = commands.Bot(command_prefix='!')  # '!' will be prefix for each bot commands
channels = ["commands", "general"]
status = ['your favorite music', 'Fifa', 'Clash Royale']

#events
@bot.event
async def on_ready():
    change_status.start()
    print(f'**{bot.user.name} is now online**')
    # Here get() takes the iterable and some keyword arguments. The keyword arguments represent attributes of the elements in the iterable that must all be satisfied for get() to return statement
    # here name = GUILD is that required attribute
    #guild = discord.utils.get(bot.guilds, name = GUILD)
    # print(
    #     f'{bot.user} is connected to the following guild:\n'
    #     f'{guild.name}(id: {guild.id})\n'
    # )
    #members = '\n - '.join([member.name for member in guild.members])
    #print(f'Guild Members:\n - {members}\n\n')    
    #Changing the presence of the bot
    #await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = 'Fifa'))



@bot.event
async def on_member_join(member):
    print('member joined')
#here await will pause the execution of the surrounding coroutine until execution of each coroutine is finished 
    # await member.create_dm()  #here member.create_dm() creates a direct message channel
    # await member.dm_channel.send(    #sending the message to dm channel
    #     f' Hello {member.name}, welcome to server'
    # )
    # print(f'Member, {member} joined server {member.server}')
    channel = discord.utils.get(member.guild.channels, name='general')
    await channel.send(f'Welcome {member.mention}! to {member.guild.name}')

@bot.event
async def on_member_remove(member):
    print(f'{member} left')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(' Sorry, You do not have correct role for this command!')



#for private messages # if I uncomment these then commands wont work?
@bot.event
async def on_message(message):
   
   #to get message in console
    author = message.author
    content = message.content
    print(f'{author}: {content}')
    if author == bot.user:
        return

    welcome_quotes = ['I am Fine', 'I am awesome', 'Allright here']
    #channels = ["commands", "general"]
    
    if content == 'how are you':
        response = random.choice(welcome_quotes)
        await message.channel.send(response)
    elif content == 'Hi':
        response = f'Hello {message.author.name}'
        await message.channel.send(response)
    elif content == 'raise-exception': #to raise exception on command 
        raise discord.DiscordException

    await bot.process_commands(message) 


@bot.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel 

    await channel.send(f'{author.name} deleted message \'{content}\'')
    


#commands for guild
##### Default welcome command ####
@bot.command(aliases=['hello','hi','namaste','hey'], help='\nWelcomes you to the server')
async def say_hello(ctx): #ctx i-e context is a must parameter for any command function. It holds data such as the channel and the guild that the user called the command from
    response = f'Hello {ctx.author.name}, How are you?'
    await ctx.send(response)

@bot.command(name="die", help="\nreturns random last words")
async def die(ctx):
    responses = ['Why have you brought my short life to end', 'Noooooo', 'I could have done so much']
    await ctx.send(choice(responses))

@bot.command(name="credits", help="\nCredits to Developer")
async def credits(ctx):
    await ctx.send('Developed By: `Anish Shilpakar`')
    await ctx.send('Thanks for using us')

##### ADMIN  COMMANDS #####
@bot.command(name='create_channel', help='\nAllows creating channels in the server for admin')
@commands.has_role('admin')
async def create_channel(ctx, channel_type='text', channel_name=f'New-channel{random.randint(1,1000)}'):
    guild = ctx.guild
    print(guild.name)
    print(guild.channels)    
    existing_channel = discord.utils.get(guild.channels, name=channel_name.lower())
    print(existing_channel)
    if not existing_channel:
        print(f'Creating a new channel : {channel_name}')
        if channel_type == 'text':
            await guild.create_text_channel(channel_name)
            await ctx.send(f'{channel_name} has been created successfully')
        elif channel_type == 'voice':
            await guild.create_voice_channel(channel_name)
            await ctx.send(f'{channel_name} has been created successfully')
        else:
            await ctx.send(f'{channel_type} is not a valid channel type.\nTry using text or voice')        
    else:
        await ctx.send(f'{channel_name} already exists.\nTry creating another channel') 

@bot.command(name='users', help='\nshow all members')
async def show_user(ctx):
    print(ctx.channel)
    if str(ctx.channel) in channels:
        guild = ctx.guild
        print(guild.name)
        print(guild.members)
        await ctx.send(f'No of members: {guild.member_count}\n')
    

###### GENERAL COMMANDS #####
@bot.command(name='roll_dice', help='\nSimulates rolling dice. e.g. !roll_dice 2 6 will simulate 2 dices with 6 sides')
async def roll(ctx, number_of_dice= 1, number_of_sides= 6):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice)) #join() returns a string in which the elemnts of a sequence have been seperated by string seperator

@bot.command(name='flip_coin', help='\nSimulates flipping a coin. e.g. !flip_coin 2 will simulate flipping 2 coins')
async def flip(ctx, number_of_coins=1):
    coin_sides = ['Heads', 'Tails']
    coin = [
        random.choice(coin_sides)
        for i in range(number_of_coins)
    ]
    await ctx.send(', '.join(coin))

@bot.command(name='joke', help='\nGets you a joke')
async def tell_joke(ctx):
    joke =  joke_api.get_joke()

    if joke == False:
        await ctx.send('Sorry due to some technical problem I couldn\'t get a joke for you. Please try again')
    else:
        await ctx.send(joke['setup'] + '\n' + joke['punchline'])    

@bot.command(name='quote', help='\nGets you a random quote')
async def tell_quote(ctx):
    quote =  quotes_api.get_quote()

    if quote == False:
        await ctx.send('Sorry due to some technical problem I couldn\'t get a quote for you. Please try again')
    else:
        await ctx.send(quote['text'] + '\n -' + quote['author'])


@bot.command(name = 'ping_web', help='\nprovides ping statistics for given website')
async def getPing(ctx, website_url="discord.com"):
    ping_stats = check_ping.checkPing(website_url)
    #print(ping_stats["packet_transmit"])
    if ping_stats == False: 
        await ctx.send('Sorry due to some technical issue, I cannot fetch ping statistics. Please Try again')
    else:
        await ctx.send(f'Pong!\n Ping details for "{website_url}" :\n Packets transmitted : {ping_stats["packet_transmit"]} \n Packets Received : {ping_stats["packet_receive"]}\n Packet Loss : {ping_stats["packet_loss_count"]}%\n Packet Loss Rate : {ping_stats["packet_loss_rate"]}\n rtt min/avg/max/mdev = {ping_stats["rtt_min"]}/{ping_stats["rtt_avg"]}/{ping_stats["rtt_max"]}/{ping_stats["rtt_mdev"]}\n')

@bot.command(name='ping', help="\nreturns latency ")
async def ping(ctx):
    await ctx.send(f'**Pong!**\n Latency : {round(bot.latency *1000)} ms')

@bot.command(name="echo", help="\nwill just echo/print")
async def echo(ctx, *, arg):
    await ctx.send(arg)
    #eqvt code
    # async def echo(ctx, *args):
    #     output = ''
    #     for word in args:
    #         output += word
    #         output += ' '
    #     await ctx.send(output)    
    #     await bot.say(output)  

@bot.command(name="time", help="\ngives current time")
async def get_time(ctx,timezone="Asia/Kathmandu"):
    inputTimeZone = pytz.timezone(timezone)
    now = datetime.now(inputTimeZone)
    current_time = now.strftime("%H:%M:%S")
    await ctx.send(f"Current time : {current_time}")

@bot.command(name="date", help="\ngives current date")
async def get_date(ctx):
    today = date.today()
    today_date = today.strftime("%B %d %Y")
    await ctx.send(f"Today is {today_date}")

@bot.command(aliases=['bye','goodbye','getout'], help="\nsays goodbye")
async def say_bye(ctx):
    response = f"Good bye {ctx.author.name}. See you later"
    await ctx.send(response)

@bot.command(name="weather", help="\ngives the weather for given location. Default: Kathmandu")
async def tell_weather(ctx, city="Kathmandu"):
    weather_data = weather_api.get_weather(city)
    if weather_data == False:
        await ctx.send('Sorry due to some technical problem I couldn\'t get weather info for you. Please try again')
    else:
        weather_details = weather_data['main']
        weather_report = weather_data['weather']
        print(weather_details)
        temperatureInCelsius = (int(weather_details["temp"]) - 273)
        response = f'Weather Report for {city} :\n Weather Condition: {weather_report[0]["description"]}\n Temperature : {temperatureInCelsius} C \n Humidity: {weather_details["humidity"]} % \n Pressure: {weather_details["pressure"]} atm\n'
        await ctx.send(response)

@bot.command(name="sun", help="\ngive details about sunrise and sunset")
async def tell_sunDetails(ctx, city="Kathmandu"):
    sun_data = weather_api.get_weather(city)
    if sun_data == False:
        await ctx.send("Sorry Due to Technical Problem, I can't get you sun details")
    else:
        sun_details = sun_data['sys']
        #print(sun_details)
        sunrise = time.localtime(sun_details['sunrise'])
        #print(sunrise.tm_hour)
        sunset = time.localtime(sun_details['sunset'])
        #print(sunset.tm_min)
        await ctx.send(f"Sun Details For {city}\n Sunrise in : {sunrise.tm_hour}:{sunrise.tm_min}:{sunrise.tm_sec}\n Sunset in : {sunset.tm_hour}:{sunset.tm_min}:{sunset.tm_sec}")

#to get random memes
#tried using an api but it was meme generator api
#same command can be used to get random images from an api
# @bot.command(name="meme", help="\nGets you a random meme")
# async def get_meme(ctx):
#     meme_data = memes_api.random_meme()
#     meme_url = meme_data["image_url"]
#     if not meme_data:
#         await ctx.send("Sorry Due to Technical Problem, I can't get you meme")
#     else:
#         await ctx.send(f'Here is a meme for you \n {meme_url}')

# I will try to get memes from reddit using praw(python reddit app wrapper)
reddit = praw.Reddit(client_id=REDDIT_APP_ID, client_secret=REDDIT_APP_SECRET, user_agent="first_discord_bot:%s:1.0" % REDDIT_APP_ID)
@bot.command(name="meme", help="gets you a random meme")
async def get_meme(ctx, str="memes"):
    async with ctx.channel.typing():
        try:
            meme_data = reddit_file.randomMeme(str)
            if not meme_data:
               await ctx.send("Technical issue")
            else:
                await ctx.send(f'Here is a meme for you\n{meme_data}')        
        except Exception as e:
            print(f'Error: \n{e}')
            await ctx.send(f'No memes were found for {str}')

###to play music ###
isConnected = False
@bot.command(name='join_channel',help='\nThe bot joins a voice channel in which user is in')
async def join_channel(ctx):
    global isConnected
    print('join caled')
    if not ctx.message.author.voice:
        await ctx.send('You are not connected to a voice channel!!! Join a channel ')
        return
    else:
        channel = ctx.message.author.voice.channel
        print(channel)
    await channel.connect()
    isConnected = True
    print('Channel Joined success')

@bot.command(name='leave_channel', help="\nbot will leave the voice channel")
async def leave_channel(ctx):
    voice_client = ctx.message.guild.voice_client
    if isConnected:
        await voice_client.disconnect()
    else:
        await ctx.send('Bot hasn\'t joined any channel yet')

#queue_of_songs for songs
queue_of_songs = []
isPlayingFromQueue = False
isPlaying = False
currentSong = ""
startingTime = 0.0
#print(len(queue_of_songs))
@bot.command(name="view_queue", help="\nShows the queue_of_songs")
async def view_queue(ctx):
    global queue_of_songs
    print(queue_of_songs)
    if len(queue_of_songs) != 0:
        i = 1
        await ctx.send('**Queue_of_songs of Songs : **\n')
        for song in queue_of_songs:
            await ctx.send(f'{i}. {song}')
            i+=1
        print(queue_of_songs)
    else:
        await ctx.send('There is nothing in queue_of_songs')
        print(queue_of_songs)
        return

@bot.command(name="queue", help="\nAdds the song to queue_of_songs")
async def queue(ctx, url=''):
    global queue_of_songs
    if len(url) != 0: 
        queue_of_songs.append(url)
        await ctx.send(f'{url} has succesully been added to queue_of_songs')
        await view_queue(ctx) 
    else:
        await ctx.send('Enter the song to add to queue')
        return

@bot.command(name="remove_song", help="\nRemoves the song from the queue_of_songs")
async def remove_song(ctx, url=''):
    global queue_of_songs
    try:
        if(len(url) != 0):
            if len(queue_of_songs)!=0:
                if url in queue_of_songs:
                    queue_of_songs.remove(url)
                    await ctx.send(f'{url} has succesfully been removed from queue_of_songs')
                    await view_queue(ctx)
                else:
                    await ctx.send(f'{url} was not found in queue_of_songs to remove')    
            else:
                await ctx.send('The queue_of_songs is empty') 
        else:
            await ctx.send('No song was provided to remove')
            return
    except:
        await ctx.send('Error while removing element from queue_of_songs')


@bot.command(name='play', help='\nThis command plays a song')
async def play(ctx, url=''):
    global isConnected,isPlaying,startingTime
    if not isConnected:
        #await ctx.send('Bot is not connected to a voice channel!!! Join a channel ')
        await join_channel(ctx)
        #return
    #await join_channel(ctx)
    print('Join success')
    global queue_of_songs,isPlayingFromQueue,currentSong
    server = ctx.message.guild
    voice_channel = server.voice_client
    if isPlaying == False:
        if (len(url) != 0):
            song_url = url
            print('Playing entered song')
        else:
            if len(queue_of_songs) != 0:
                song_url = queue_of_songs[0]
                await ctx.send('Now playing from queue')
                isPlayingFromQueue = True
                print('playing from queue')
            else:
                await ctx.send('No song in the queue please add songs before trying')
                return
        print(f'Song is {song_url}')
    
        async with ctx.typing():
            player = await YTDLSource.from_url(song_url , loop = bot.loop)
            print(player)
            await ctx.send(f'**Now Playing:** {player.title}')
            voice_channel.play(player, after=lambda e: print('Player Error: %s' % e) if e else None)
            #startingTime = time.perf_counter()
        
        currentSong = player.title
        isPlaying = True
        print(f'Video Duration: {videoDuration}')

    print(1)
    if isPlayingFromQueue:
        del queue_of_songs[0]
        print(2)
    if len(queue_of_songs) != 0:    
        print(3)
        # endTime = time.perf_counter()
        # while ((startingTime + videoDuration) > endTime):
        #     if (startingTime + videoDuration) < endTime:
        #         break
        #     else:
        #         continue
        startingTime = threading.Timer(10,playInQueue(ctx))          
        await ctx.send('Now playing from queue after this song')
        #await skip(ctx)
        startingTime.start()
        print('4')
        
def playInQueue(ctx):
    print("palying from queue now")
    asyncio.create_task(skip(ctx))

@bot.command(name='stop', help='\nStop the playing song')
async def stop(ctx):
    global queue_of_songs,isPlaying
    server = ctx.message.guild
    voice_channel = server.voice_client
    if isPlaying:
        voice_channel.stop()
        await ctx.send(f'The Song has been stopped')
        isPlaying = False
    else:
        await ctx.send('No song is being played yet')    
    
@bot.command(name='pause', help='\nPauses the playing song')
async def pause(ctx):
    global queue_of_songs,isPlaying
    server = ctx.message.guild
    voice_channel = server.voice_client
    if isPlaying:
        voice_channel.pause()
        await ctx.send(f'song has succesfully been Paused')
        isPlaying = False
    else:
        await ctx.send('No song is being played')

@bot.command(name='resume', help='\nResumes playing song')
async def resume(ctx):
    global queue_of_songs,isPlaying
    server = ctx.message.guild
    voice_channel = server.voice_client
    if not isPlaying:
        voice_channel.resume()
        await ctx.send(f'Resuming the song')
        isPlaying = True

@bot.command(name='skip', help="\nSkips the song in the queue")
async def skip(ctx):
    global queue_of_songs, isPlayingFromQueue
    server = ctx.message.guild
    voice_channel = server.voice_client
    voice_channel.stop()
    print('in skip')
    if len(queue_of_songs) != 0:
        print('in skip')
        if isPlayingFromQueue:
            await ctx.send('Playing Next Song:\n')
            await play(ctx)
        else:
            await ctx.send('Playing from queue now:\n')
            await play(ctx)    
    else:
        await ctx.send('The Queue is empty !!! Please Add songs before skipping')
    
#changing the bot status
@tasks.loop(seconds=30)
async def change_status():
    #Changing the presence of the bot
    if currentSong == "":
        await bot.change_presence(activity = discord.Game(choice(status)))
    else:
        await bot.change_presence(activity = discord.Game(currentSong))

bot.run(TOKEN)     
