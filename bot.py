#!/usr/bin/env python3

import asyncio
import discord
import random
import os
import sys
import re

from google_images_download import google_images_download

from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt

from datetime import datetime
from discord.ext import commands


bot = commands.Bot(command_prefix="!")


def is_admin(user):
    """
    Checks whether user is an administrator on the guild 
    """
    return user.guild_permissions.administrator


@bot.event
async def on_message(message):
    """
    Fill up 'log.txt' with messages as they are sent in channels with bot
    TODO: - Add separate log.txts for separate channels:w
          - Clear log files as they get too large
    """

    message_content = message.content
    with open("log.txt", "a") as f:
       time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       f.write(f"<{time_stamp}>{message_content}\n")
    await bot.process_commands(message)


@commands.command()
async def ping(ctx):
    """
    Pings the bot
    """
    await ctx.send(':ping_pong:')


@commands.command()
async def echo(ctx, n=0, *, content:str):
    """
    Echoes a message, !echo [amount of times to echo] [message here]
    """
    print('{} - Command: echo | Author: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ctx.author))
    index = 0
    limit = 15
    if n > 0:
        while index < min(n,limit):
            await ctx.send(content)
            index += 1
    else:
        await ctx.send(content)
    print('{} - Task Finished Succesfully'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


@commands.command()
async def coinflip(ctx):
    """
    Flip a coin
    """
    options=['Heads','Tails']
    await ctx.send('You rolled ' + options[random.randint(0,1)])


@commands.command()
async def google(ctx, *, keywords:str):
    """
    Finds a random google image with a given keyword
    """
    print('{} - Command: google | Author: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ctx.author))
    response = google_images_download.googleimagesdownload()   #class instantiation

    arguments = {"keywords":keywords,"limit":5,"print_urls":False, "format":"jpg", "safe_search":True}   #creating list of arguments
    paths = response.download(arguments)   #passing the arguments to the function
    my_files = [
    discord.File(paths[0][keywords][random.randint(0,4)]),
    ]

    await ctx.send(files=my_files)
    print('{} - Task Finished Succesfully'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


@commands.command()
async def wordcloud(ctx):
    """
    Creates a worldcloud from the last 5000 messages
    """
    print('{} - Command: wordcloud | Author: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ctx.author))
    cache_size = len(bot.cached_messages)
    
    print(f'cache type: {type(bot.cached_messages)}')
    print(f'cache size: {cache_size}')
    
    messages = []

    for message in bot.cached_messages: # returns a discord.Message object
            messages.append(message.content)

    text = ' '.join(messages)
   
    if os.path.exists('word_cloud.png'):
        os.remove('word_cloud.png')

    wordcloud = WordCloud(max_font_size=50, max_words=500, background_color="white").generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    wordcloud.to_file('word_cloud.png')

    
@commands.command()
async def wolfram(ctx, *, content:str):
    """
    Returns the search result from wolfram alpha based on keyword(s)
    """
    print('{} - Command: wolfram | Author: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ctx.author))
    wolfram_app_id = 'JE3KG9-QAQ9KVK5X6'
    wolfram_url = 'https://api.wolframalpha.com/v1/result'
    wolfram_params = {'i':'{}'.format(content),'appid':'{}'.format(wolfram_app_id)}

    print('Request: '+ content)

    r = requests.get(wolfram_url, params=wolfram_params)
    await ctx.send(r.text)
    print('{} - Task Finished Succesfully'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


@commands.command()
async def wolfram_image(ctx, *, content:str):
    """
    Returns the search result as an image from wolfram alpha based on keyword(s)
    """
    print('{} - Command: wolfram_image | Author: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ctx.author))
    wolfram_app_id = 'JE3KG9-QAQ9KVK5X6'
    wolfram_url = 'https://api.wolframalpha.com/v1/simple'
    wolfram_params = {'i':'{}'.format(content),'appid':'{}'.format(wolfram_app_id)}

    print('Request: '+ content)

    r = requests.get(wolfram_url, params=wolfram_params)
    output = open('data.gif','wb')
    output.write(r.content)
    output.close()
    file = discord.File('data.gif')

    await ctx.channel.send(file=file)
    print('{} - Task Finished Succesfully'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

    
@commands.command()
async def copypasta(ctx, filename, *, content:str):
    """
    Saves a message with a keyword as a text file
    """
    print('{} - Command: copypasta | Author: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ctx.author))
    #!copypasta pasta_name pasta
    dir = f'copypasta/{filename}.txt'
    with open(dir, 'w') as f: #save it to text file
        f.write(f'{content}\n')
    print('{} - Task Finished Succesfully'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


@commands.command()
async def pasta(ctx, filename):
    """
    Returns the message saved in a text file saved with !copypasta
    """
    print('{} - Command: pasta | Author: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ctx.author))
    dir = f'copypasta/{filename}.txt'
    with open(dir, 'r') as f:
        pasta = f.read()
        await ctx.send(pasta)
    print('{} - Task Finished Succesfully'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


@commands.command()
async def emojify(ctx, *, content:str):
   """
   Emojify the input
   """
   print('{} - Command: emoji | Author: {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),ctx.author))
   normal_text=list(content.lower())
   emoji_text = []

   for i in normal_text:
        if i == '0': 
            emoji_text.append(':zero:')
        elif i == '1': 
            emoji_text.append(':one:')
        elif i == '2': 
            emoji_text.append(':two:')
        elif i == '3': 
            emoji_text.append(':three:')
        elif i == '4': 
            emoji_text.append(':four:')
        elif i == '5': 
            emoji_text.append(':five:')
        elif i == '6': 
            emoji_text.append(':six:')
        elif i == '7': 
            emoji_text.append(':seven:')
        elif i == '8': 
            emoji_text.append(':eight:')
        elif i == '9': 
            emoji_text.append(':nine:')
        elif i == 'b':
            emoji_text.append(':b:')
        elif i == ' ':
            emoji_text.append(' ')
        elif re.search("[a-z]", i):
            emoji_text.append(':regional_indicator_{}:'.format(i))
        else:
            emoji_text.append(i)

   fullStr = ' '.join(emoji_text)
   await ctx.send(fullStr)
   print('{} - Task Finished Succesfully'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


def main():

    bot.add_command(ping)
    bot.add_command(echo)
    bot.add_command(coinflip)
    bot.add_command(google)
    bot.add_command(emojify)
    bot.add_command(wordcloud)
    bot.add_command(wolfram)
    bot.add_command(wolfram_image)
    bot.add_command(copypasta)
    bot.add_command(pasta)

    bot.run('BOT TOKEN GOES HERE')


if __name__ == "__main__":
    main()
