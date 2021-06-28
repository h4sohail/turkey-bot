import subprocess

from datetime import datetime


def logger(commandName, ctx):
    """
    commandName (Type: string): command Name name
    ctx (Type: object): Discord.context 
    """
    time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f'{time_stamp} - Command: {commandName} | Author: {ctx.message.author}')


def text_wrap(text, font, max_width):
    """
    text (Type: string): text to be added to the image
    font (Type: object): Image.Font 
    max_width (Type: int): image width 
    """
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


def is_admin(user): 
    return user.guild_permissions.administrator


def git(*args):
    return subprocess.check_call(['git'] + list(args))
