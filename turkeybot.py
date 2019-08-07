import requests
import discord
from discord.ext import commands

prefix = "!"
bot = commands.Bot(command_prefix=prefix)

@bot.event
async def on_ready():
    print("Bot is online")

@bot.command(pass_context=True)
async def ping(ctx):

    latency = bot.latency 
    await ctx.send(latency)
    
@bot.command(pass_context=True)
async def echo(ctx, *, content:str):
    
    list = content.split(':')
    
    if len(list) > 1:
        index = 0
        n = int(list[0])
        content = list[1]
        while index < n:
            await ctx.send(content)
            index += 1
    else:
        await ctx.send(list[0])

@bot.command(pass_context=True)
async def wolfram(ctx, *, content:str):

    wolframAppId = 'Wolfram API Key Here'
    wolframUrl = 'https://api.wolframalpha.com/v1/result'
    wolframParams = {'i':'{}'.format(content),'appid':'{}'.format(wolframAppId)}

    print('Request: '+ content)

    r = requests.get(wolframUrl, params=wolframParams)
    await ctx.send(r.text)

@bot.command()
async def wolfram2(ctx, *, content:str):
    
    wolframAppId = 'Wolfram API Key Here'
    wolframUrl = 'https://api.wolframalpha.com/v1/simple'
    wolframParams = {'i':'{}'.format(content),'appid':'{}'.format(wolframAppId)}

    print('Request: '+ content)

    r = requests.get(wolframUrl, params=wolframParams)
    output = open('data.gif','wb')
    output.write(r.content)
    output.close()
    file = discord.File('data.gif', filename='data.gif')

    await ctx.channel.send('data.gif',file=file)

@bot.command(pass_context=True)
async def emoji(ctx, *, content:str):
   
   normalText=list(content.lower())
   emojiText = []

   for i in normalText:
        if i == 'b':
            emojiText.append(':b:')
        else:
            emojiText.append(':regional_indicator_{}:'.format(i))

   fullStr = ' '.join(emojiText)
   await ctx.send(fullStr)

bot.run('Client Token Here')