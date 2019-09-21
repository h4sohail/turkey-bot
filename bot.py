#!/usr/bin/env python3

import asyncio, random, time, re, os, sys, json, shutil
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import discord
import youtube_dl
import requests

from discord import FFmpegPCMAudio
from discord.ext import commands, tasks
from discord.utils import get
from datetime import datetime
from itertools import cycle
from google_images_download import google_images_download
from PIL import Image, ImageDraw, ImageFont
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# command prefix, bot initialization and removal of default 'help' command
prefix = '!'
bot = commands.Bot(command_prefix=prefix)
bot.remove_command('help')

# status cycle
status = cycle(['Hacking the NSA', 'Serving Healthy Food', 'Serving Pizza Again'])

# global variables
wash_cycle = False  
user = None

vote = False # votemute active or not
votes = {'yes':0, 'no':0} # vote tally
voters = [] # list of voters
muted = {} # list of muted people

u_vote = False # voteunmute active or not
u_votes = {'yes':0, 'no':0} # vote tally
u_voters = [] # list of voters


@bot.event
async def on_ready(): # runs upon bot being initialized
    status_loop.start() # start status_loop
    auto_unmute.start() # start auto_unmute loop
    muted_list_export.start() # start muted_list_export loop
    print(f'{bot.user.name}#{bot.user.discriminator} is online')
    print(f'discord.py version: {discord.__version__}')


@bot.event
async def on_member_join(member): # runs when a new member joins the server
    if member in muted: # checks if member is in the muted list
        role = discord.utils.get(member.guild.roles, name='muted by the people') # gets the role name
        await  member.add_roles(role) # assigns the role
    else:
        pass # TO-DO: add a default 'member' role to all users upon joining


@bot.event
async def on_message(message): # runs on a new message being sent in the server
    global votes
    global voters
    global u_votes
    global u_voters
    
    message_content = message.content # store message content in a variable
    author = message.author # grab the author name from the message
    if author == bot.user: # make sure the message was not sent by the bot
        return

    if vote: # check if votemute is active
        if (message_content == 'yes') and not(author in voters): # check if someone typed 'yes'
            votes['yes'] = votes['yes'] + 1 # add 1 to votes counter
            voters.append(author) # add author to voters list
            print(f'{author} voted yes')

        elif (message_content == 'no') and not(author in voters): # check if someone typed 'no'
            votes['no'] = votes['no'] + 1 # add 1 to the no counter
            voters.append(author) # add author to voters list
            print(f'{author} voted no')

    elif u_vote: # check if voteunmute is active
        if (message_content == 'yes') and not(author in u_voters):
            u_votes['yes'] = u_votes['yes'] + 1
            u_voters.append(author)
            print(f'{author} voted yes')

        elif (message_content == 'no') and not(author in u_voters):
            u_votes['no'] = u_votes['no'] + 1
            u_voters.append(author)
            print(f'{author} voted no')
    
    else:
        pass # TO-DO:To be decided
      
    dir = 'cache\log.txt' # log all messages sent in the server with a time stamp in the format YYYY:MM:DD HH:MM:SS
    with open(dir, 'a') as f:
       time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       f.write(f"<{time_stamp}>{message_content}\n")

    await bot.process_commands(message) # tells bot to process the custom commands below


@tasks.loop(seconds=10) 
async def status_loop(): # changes the bot's status every 10 seconds
    await bot.change_presence(activity=discord.Game(next(status)))


@tasks.loop(seconds=10) # TO-DO
async def muted_list_export(): # exports the list of muted users every 10 seconds
    muted_json = json.dumps(muted) # this function needs work, is not finished yet.
    dir = 'muted.json'
    with open(dir, 'w+') as f:
        json.dump(muted_json, f)


@tasks.loop(seconds=10) # TO-DO
async def muted_list_import(): # imports the list of muted users every 10 seconds
    #global
    #dir = 'muted.json'
    #with open(dir, 'w+') as f:
        #muted = json.load(f)
    pass

@tasks.loop(seconds=10) # TO-DO
async def auto_unmute(): # auto unmutes people and updates the muted 
    for member in muted:
        if time.time() - muted[member] >= 900:
            role = discord.utils.get(member.guild.roles, name='muted by the people')
            await  member.remove_roles(role)
            print(f'auto_unmuted: unmuted {member}')
            del muted[member]


def logger(func, ctx, start):
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if start == True:
        print(f'{time_stamp} - Command: {func} | Author: {ctx.message.author}')
    else:
        print(f'{time_stamp} - Task Finished Succesfully')


def text_wrap(text, font, max_width):
    lines = []
    # If the width of the text is smaller than image width
    # we don't need to split it, just add it to the lines array
    # and return
    if font.getsize(text)[0] <= max_width:
        lines.append(text) 
    else:
        # split the line by spaces to get words
        words = text.split(' ')  
        i = 0
        # append every word to a line while its width is shorter than image width
        while i < len(words):
            line = ''         
            while i < len(words) and font.getsize(line + words[i])[0] <= max_width:                
                line = line + words[i] + " "
                i += 1
            if not line:
                line = words[i]
                i += 1
            # when the line gets longer than the max width do not append the word, 
            # add the line to the lines array
            lines.append(line)    
    return lines

#checks if a user is an administrator
def is_admin(user): 
    """
    Checks if the user is an administrator
    """
    return user.guild_permissions.administrator

#clears the cache and restarts the bot
@commands.command()
async def reset(ctx):
    logger('reset',ctx,True)
    
    if is_admin(ctx.message.author):
        bot.clear() # clear internal cache
        shutil.rmtree('/home/ubuntu/dining_services_bot/downloads') # delete cached google images
        await ctx.send('cache cleared')
        await ctx.send('restarting the bot')
        os.execv('/home/ubuntu/dining_services_bot/bot.py', sys.argv) # restart the bot
    else:
        await ctx.send('you are not authorized to use this command :rage:')

    logger('reset',ctx,False)


@commands.command()
async def votemute(ctx, member:discord.Member=None):
    logger('votemute',ctx,True)
    
    global vote
    global votes
    global voters
    global muted
    guild = ctx.guild # get guild(server) information
    if vote or u_vote: # make sure only 1 voting session is active at a time
        await ctx.send('a vote is already in progress, please wait')
        return
        
    vote = True 

    await ctx.send(f'vote to mute started by {ctx.message.author}')
    await ctx.send('reply with [yes] or [no] to vote')

    await ctx.send('waiting 60 seconds for votes')
    await asyncio.sleep(30)
    
    await ctx.send('waiting 30 seconds for votes')
    await asyncio.sleep(20)

    await ctx.send('waiting 10 seconds for votes')
    await asyncio.sleep(10)

    yes_votes = votes['yes'] # get amount of yes votes
    no_votes = votes['no'] # get amount of no votes

    if yes_votes > no_votes: # compare results
        await ctx.send('the majority has voted yes, user will be muted for 15 minutes')
        
        role = discord.utils.get(member.guild.roles, name='muted by the people') # get the muted role
        await  member.add_roles(role) # assign the muted role
        muted[member] = time.time() # add member to the muted list with a time stamp
        print(f'{member} has been muted for 15 minutes')
        for invite in await guild.invites(): # remove muted users invites
            if invite.inviter == member:
                await invite.delete()
            else:
                pass
    if no_votes >= yes_votes:
        await ctx.send('the majority voted no, user will not be muted') 

    vote = False
    votes = {'yes':0, 'no':0}
   
    logger('votemute',ctx,False)


@commands.command()
async def voteunmute(ctx, member:discord.Member=None):
    logger('voteunmute',ctx,True)

    global u_vote
    global u_votes
    global u_voters

    if vote or u_vote:
        await ctx.send('a vote is already in progress, please wait')
        return

    u_vote = True

    await ctx.send(f'vote to mute started by {ctx.message.author}')
    await ctx.send('reply with [yes] or [no] to vote')

    await ctx.send('waiting 60 seconds for votes')
    await asyncio.sleep(30)
    
    await ctx.send('waiting 30 seconds for votes')
    await asyncio.sleep(20)

    await ctx.send('waiting 10 seconds for votes')
    await asyncio.sleep(10)

    yes_votes = u_votes['yes']
    no_votes = u_votes['no']

    if yes_votes > no_votes:
        await ctx.send('the majority has voted yes, user will be unmuted')
        role = discord.utils.get(member.guild.roles, name='muted by the people')
        await  member.remove_roles(role)
        
    print(f'{member} has been unmuted')

    if no_votes >= yes_votes:
        await ctx.send('the majority voted no, user will not be unmuted') 

    u_vote = False
    u_votes = {'yes':0, 'no':0}
       
    logger('voteunmute',ctx,False)


@commands.command()
async def giverole(ctx, role_name:str, *, color_code:str):
    ### 
    # Usage: !giverole "role name here" [html color code here]
    # You can grab the html color code from here:
    # https://www.google.com/search?q=color+picker
    # Html color codes are in the format: #0ecf43
    # Example usage: !giverole "green is the best" #0ecf43   
    ###
    logger('giverole',ctx,True)
    
    if color_code == '#000000': # discord.py was having issues with this color code
        color_code = '#111111'
        print(f'Color Code Exception 0. Color Replaced With: {color_code}')
    else:
        pass

    color_code = color_code.split('#') # remove the #
    color_code.insert(0, '0x') # replace it with 0x
    color_code = ''.join(color_code) # join the string back
    color_code = int(color_code, 16) # cast to base 16 int

    guild = ctx.guild
    member = ctx.author
    role = discord.utils.get(member.guild.roles, name=role_name)

    if role not in guild.roles: # if role doesnt exist, create it
        await guild.create_role(name=role_name,color=discord.Colour(color_code))
    
    if role == None:
        await ctx.send('something went wrong :D')
    
    await member.add_roles(role) # assign the role to the member
    await ctx.send('role added')

    logger('giverole',ctx,False)


@commands.command()
async def removerole(ctx, role_name:str):
    logger('removerole',ctx,True)

    member = ctx.author
    role = discord.utils.get(member.guild.roles, name=role_name)
    if role is None:
        await ctx.send('something went wrong :D')
    else:
        await  member.remove_roles(role)
        await ctx.send('role removed')

    logger('removerole',ctx,False)


@commands.command()
async def wordcloud(ctx):
    logger('wordcloud',ctx,True)
    
    messages = [] 

    for message in bot.cached_messages: # grab all the messages from the bot's internal cache
            messages.append(message.content)

    text = ' '.join(messages)
   
    if os.path.exists('word_cloud.png'): # delete the last word cloud
        os.remove('word_cloud.png')

    wordcloud = WordCloud(max_font_size=50, max_words=500, background_color="white").generate(text) # generate the wordcloud
    plt.figure() # draw the wordcloud
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    wordcloud.to_file('word_cloud.png') # save the wordcloud as an image file

    file = discord.File('word_cloud.png') # create an attachment
    await ctx.channel.send(file=file) # send the attachment
    
    logger('wordcloud',ctx,False)


@commands.group() 
async def meme(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('invalid command :D')


@meme.command()
async def clown(ctx, *, text:str):
    logger('clown',ctx,True)

    img = Image.open('resources/clown.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('resources/arial.ttf', 55)
    image_size = img.size
    lines = text_wrap(text, font, image_size[0])
    line_height = font.getsize('hg')[1]

    x = 0
    y = 0
    color = (0,0,0)
    for line in lines:
        # draw the line on the image
        draw.text((x, y), line, fill=color, font=font)
        # update the y position so that we can use it for next line
        y = y + line_height

    img.save('resources/clown_edit.jpg')
    file = discord.File('resources/clown_edit.jpg')

    await ctx.channel.send(file=file)

    logger('clown',ctx,False)


@meme.command()
async def ghandi(ctx, *, text:str):
    logger('ghandi',ctx,True)

    img = Image.open('resources/ghandi.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('resources/arial.ttf', 60)
    image_size = img.size
    lines = text_wrap(text, font, image_size[0])
    line_height = font.getsize('hg')[1]

    x = 0
    y = 0
    for line in lines:
        color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        # draw the line on the image
        draw.text((x, y), line, fill=color, font=font)
        # update the y position so that we can use it for next line
        y = y + line_height

    img.save('resources/ghandi_edit.jpg')
    file = discord.File('resources/ghandi_edit.jpg')

    await ctx.channel.send(file=file)

    logger('ghandi',ctx,False)


@meme.command()
async def dougford(ctx, *, text:str):
    logger('dougford',ctx,True)

    img = Image.open('resources/dougford.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('resources/arial.ttf', 55)
    image_size = img.size
    lines = text_wrap(text, font, image_size[0])
    line_height = font.getsize('hg')[1]

    x = 0
    y = 0
    color = (0,0,0)
    for line in lines:
        # draw the line on the image
        draw.text((x, y), line, fill=color, font=font)
        # update the y position so that we can use it for next line
        y = y + line_height

    img.save('resources/dougford_edit.jpg')
    file = discord.File('resources/dougford_edit.jpg')

    await ctx.channel.send(file=file)

    logger('dougford',ctx,False)


@meme.command()
async def robford(ctx, *, text:str):
    logger('robford',ctx,True)

    img = Image.open('resources/robford.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype('resources/arial.ttf', 55)
    image_size = img.size
    lines = text_wrap(text, font, image_size[0])
    line_height = font.getsize('hg')[1]

    x = 0
    y = 0
    color = (0,0,0)
    for line in lines:
        # draw the line on the image
        draw.text((x, y), line, fill=color, font=font)
        # update the y position so that we can use it for next line
        y = y + line_height

    img.save('resources/robford_edit.jpg')
    file = discord.File('resources/robford_edit.jpg')

    await ctx.channel.send(file=file)

    logger('robford',ctx,False)


@commands.command()
async def ping(ctx):
    logger('ping',ctx,True)

    latency = bot.latency 
    await ctx.send(latency)
    await ctx.send(':ping_pong:')

    logger('ping',ctx,False)


@commands.command()
async def echo(ctx, n:int, *, content:str):
    logger('echo',ctx,True)

    index = 0
    limit = 15
    if n > 0:
        
        while index < min(n,limit):
            await ctx.send(content)
            index += 1
    else:
        await ctx.send(content)

    logger('echo',ctx,False)


@commands.command()
async def copypasta(ctx, *, content:str):
    logger('copypasta',ctx,True)

    try:
        #!copypasta pasta_name pasta
        filename = re.sub('\W+',' ',(content.split()[0]))
        print(f'file name: {filename}')
        pasta = content.split() # get the copypasta from input
        del pasta[0]
        pasta_string = ' '.join(pasta) 
        print(f'pasta string: {pasta_string}')
        dir = f'copypasta/{filename}.txt'
        with open(dir, 'w') as f: #save it to text file
           f.write(f'{pasta_string}\n')
    except:
        print('something went wrong')

    logger('copypasta',ctx,False)


@commands.command()
async def pasta(ctx, filename):
    logger('pasta',ctx,True)

    dir = f'copypasta/{filename}.txt'
    with open(dir, 'r') as f:
        pasta = f.read()
        await ctx.send(pasta)

    logger('pasta',ctx,False)


@commands.command()
async def wolfram(ctx, *, content:str):
    logger('wolfram',ctx,True)

    wolframAppId = 'JE3KG9-QAQ9KVK5X6'
    wolframUrl = 'https://api.wolframalpha.com/v1/result'
    wolframParams = {'i':'{}'.format(content),'appid':'{}'.format(wolframAppId)}

    print('Request: '+ content)

    r = requests.get(wolframUrl, params=wolframParams)
    await ctx.send(r.text)

    logger('wolfram',ctx,False)


@commands.command()
async def wolfram2(ctx, *, content:str):
    logger('wolfram2',ctx,True)

    wolframAppId = 'JE3KG9-QAQ9KVK5X6'
    wolframUrl = 'https://api.wolframalpha.com/v1/simple'
    wolframParams = {'i':'{}'.format(content),'appid':'{}'.format(wolframAppId)}

    print('Request: '+ content)

    r = requests.get(wolframUrl, params=wolframParams)
    output = open('data.gif','wb')
    output.write(r.content)
    output.close()
    file = discord.File('data.gif')

    await ctx.channel.send(file=file)
    
    logger('wolfram2',ctx,False)


@commands.command()
async def google(ctx, *, keywords:str):
    logger('google',ctx,True)
    
    response = google_images_download.googleimagesdownload()   #class instantiation

    arguments = {"keywords":keywords, "limit":5,"print_urls":False, "format":"jpg", "safe_search":True}   #creating list of arguments
    paths = response.download(arguments)   #passing the arguments to the function
    my_files = [
    discord.File(paths[0][keywords][random.randint(0,4)]),
    ]

    await ctx.send(files=my_files)

    logger('google',ctx,False)


@commands.command()
async def youtube(ctx, *, url:str):
    logger('youtube',ctx,True)

    if os.path.exists('source.m4a'):
        os.remove('source.m4a')

    def hook(d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')

    options = {
        'restrictfilenames' : 'True',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
            'preferredquality': '192',
        }],
        'progress_hooks': [hook]
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download(['{}'.format(url)])

    for file in os.listdir(os.getcwd()):
        if file.endswith('.m4a'):
            print(file)
            os.rename (str(file), 'source.m4a')
    try:
        channel = ctx.message.author.voice.channel
    
        if not channel:
            await ctx.send('You are not connected to a voice channel')

        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()
        source = FFmpegPCMAudio('source.m4a')
        player = voice.play(source)
    except:
        await ctx.send('You are not connected to a voice channel')

    logger('youtube',ctx,False)


@commands.command()
async def succ(ctx):
    logger('succ',ctx,True)

    try:
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send('You are not connected to a voice channel')

        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
                await voice.move_to(channel)
        else:
            voice = await channel.connect()
        source = FFmpegPCMAudio('sounds/succ.m4a')
        player = voice.play(source)
    except:
        await ctx.send('You are not connected to a voice channel')

    logger('succ',ctx,False)


@commands.command()
async def oof(ctx):
    logger('oof',ctx,True)

    try:
        channel = ctx.message.author.voice.channel
        if not channel:
            await ctx.send('You are not connected to a voice channel')

        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
                await voice.move_to(channel)
        else:
            voice = await channel.connect()
        source = FFmpegPCMAudio('sounds/roblox.m4a')
        player = voice.play(source)
    except:
        await ctx.send('You are not connected to a voice channel')

    logger('oof',ctx,False)


@commands.command()
async def flip(ctx):
    logger('flip',ctx,True)

    options=['Heads','Tails']
    await ctx.send('You rolled ' + options[random.randint(0,1)])

    logger('flip',ctx,False)


@commands.command()
async def disconnect(ctx):
    logger('disconnect',ctx,True)

    voice = get(bot.voice_clients, guild=ctx.guild)
    await voice.disconnect()
    if os.path.exists('source.m4a'):
        os.remove('source.m4a')

    logger('disconnect',ctx,False)


@commands.command()
async def emoji(ctx, *, content:str):
   logger('emoji',ctx,True)

   normalText=list(content.lower())
   emojiText = []

   for i in normalText:
        if i == '0': 
            emojiText.append(':zero:')
        elif i == '1': 
            emojiText.append(':one:')
        elif i == '2': 
            emojiText.append(':two:')
        elif i == '3': 
            emojiText.append(':three:')
        elif i == '4': 
            emojiText.append(':four:')
        elif i == '5': 
            emojiText.append(':five:')
        elif i == '6': 
            emojiText.append(':six:')
        elif i == '7': 
            emojiText.append(':seven:')
        elif i == '8': 
            emojiText.append(':eight:')
        elif i == '9': 
            emojiText.append(':nine:')
        elif i == 'b':
            emojiText.append(':b:')
        elif i == ' ':
            emojiText.append(' ')
        elif re.search("[a-z]", i):
            emojiText.append(':regional_indicator_{}:'.format(i))
        else:
            emojiText.append(i)

   fullStr = ' '.join(emojiText)
   await ctx.send(fullStr)

   logger('emoji',ctx,False)


@commands.command()
async def help(ctx):
    logger('help',ctx,True)

    embed = discord.Embed(title='Available Commands')

    embed.add_field(name='!ping', value='returns the ping', inline = False)
    embed.add_field(name='!echo', value='usage: !echo [number of times to echo] [text to echo]', inline = False)
    embed.add_field(name='!giverole', value='usage: !giverole "name here" [html color code]', inline = False)
    embed.add_field(name='!removerole', value='usage: !removerole "name here"', inline = False)
    embed.add_field(name='!flip', value='flips a coin', inline = False)
    embed.add_field(name='!copypasta', value='usage: !copypasta [name] [copypasta here]', inline = False)
    embed.add_field(name='!pasta', value='recall the copypasta, !pasta [name]')
    embed.add_field(name='!emoji', value='emojifys the text', inline = False)
    embed.add_field(name='!wordcloud', value='generates a wordcloud', inline = False)
    embed.add_field(name='!wolfram', value='wolfram search', inline = False)
    embed.add_field(name='!wolfram2', value='wolfram search but returns an image', inline = False)
    embed.add_field(name='!google', value='usage: !google [keywords]', inline = False)
    embed.add_field(name='!youtube', value='usage: !youtube [youtube link]', inline = False)
    embed.add_field(name='!disconnect', value='disconnects the bot from the voice channel', inline = False)
    embed.add_field(name='!meme ghandi', value='usage: !ghandi (text)', inline = False)
    embed.add_field(name='!meme dougford', value='usage: !dougford (text)', inline = False)
    embed.add_field(name='!meme robford', value='usage: !robford (text)', inline = False)
    embed.add_field(name='!meme clown', value='usage: !clown (text)', inline = False)
    embed.add_field(name='!votemute', value='usage: !votemute (tag the user to mute)', inline = False)
    embed.add_field(name='!voteunmute', value='usage: !voteunmute (tag the user to mute)', inline = False)

    await ctx.send(embed=embed)

    logger('help',ctx,False)

 
def main():
    
    bot.add_command(ping)
    bot.add_command(echo)
    bot.add_command(giverole)
    bot.add_command(removerole)
    bot.add_command(flip)
    bot.add_command(copypasta)
    bot.add_command(pasta)
    bot.add_command(emoji)
    bot.add_command(wordcloud)
    bot.add_command(wolfram)
    bot.add_command(wolfram2)
    bot.add_command(google)
    bot.add_command(youtube)
    bot.add_command(disconnect)
    bot.add_command(ghandi)
    bot.add_command(dougford)
    bot.add_command(robford)
    bot.add_command(clown)
    bot.add_command(meme)
    bot.add_command(votemute)
    bot.add_command(voteunmute)

    bot.run('Discord_Bot_Token_Here')

if __name__ == "__main__":
    main()
