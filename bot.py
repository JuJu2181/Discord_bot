#connecting a bot to a channel
#Bot is a subclass of Client with added functions

import os
import random
import discord
from dotenv import load_dotenv

import joke_api

#1
from discord.ext import commands
#from bot_life import keep_alive

#keep_alive()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#TOKEN = 'NzMyOTgxMzAzMTYyNDM3NzMz.XxVpYQ.SanIqXTlntglEgRG0_vtauLXG58'
#GUILD = 'Python_App_Tests'

#2
bot = commands.Bot(command_prefix='!')  # '!' will be prefix for each bot commands

#events
@bot.event
async def on_ready():
    print(f'{bot.user.name} bot has connected to Discord!')
    # Here get() takes the iterable and some keyword arguments. The keyword arguments represent attributes of the elements in the iterable that must all be satisfied for get() to return statement
    # here name = GUILD is that required attribute
    guild = discord.utils.get(bot.guilds, name = GUILD)
    print(
        f'{bot.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}\n\n')    
    #Changing the presence of the bot
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.playing, name = 'Fifa'))
    
@bot.event
async def on_member_join(member):
#here await will pause the execution of the surrounding coroutine until execution of each coroutine is finished 
    await member.create_dm()  #here member.create_dm() creates a direct message channel
    await member.dm_channel.send(    #sending the message to dm channel
        f' Hello {member.name}, welcome to {GUILD}'
    )
    print(f'Member, {member} joined server')

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
@bot.command(aliases=['hello','hi','namaste','hey'], help='Welcomes you to the server')
async def say_hello(ctx): #ctx i-e context is a must parameter for any command function. It holds data such as the channel and the guild that the user called the command from
    response = f'Hello {ctx.author.name}, welcome to {GUILD}'
    await ctx.send(response)

@bot.command(name='create_channel', help = 'Allows creating channels in the server for admin')
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

@bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    response = random.choice(brooklyn_99_quotes)
    await ctx.send(response)


@bot.command(name='roll_dice', help='Simulates rolling dice. e.g. !roll_dice 2 6 will simulate 2 dices with 6 sides')
async def roll(ctx, number_of_dice= 1, number_of_sides= 6):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    await ctx.send(', '.join(dice)) #join() returns a string in which the elemnts of a sequence have been seperated by string seperator

@bot.command(name='flip_coin', help='Simulates flipping a coin. e.g. !flip_coin 2 will simulate flipping 2 coins')
async def flip(ctx, number_of_coins=1):
    coin_sides = ['Heads', 'Tails']
    coin = [
        random.choice(coin_sides)
        for i in range(number_of_coins)
    ]
    await ctx.send(', '.join(coin))

@bot.command(name='joke', help='Gets you a joke')
async def tell_joke(ctx):
    joke = joke_api.get_joke()

    if joke == False:
        await ctx.send('Sorry due to some technical problem I couldn\'t get a joke for you. Please try again')
    else:
        await ctx.send(joke['setup'] + '\n' + joke['punchline'])    

@bot.command(name = 'ping')
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command(name="echo")
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



bot.run(TOKEN)     
