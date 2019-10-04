# Turkey Bot
Simple bot for Discord written in Python3 to be ran on a linux based environment with Python3 and FFmpeg installed
# Usage
Install Python3 and FFmpeg  
Fork the project and modify it as needed.  
Run the project as ```python3 bot.py bot_token_here```  
# Requirements
Refer to requirements.txt
# Commands
!ping: Returns the ping  
- example: !ping  

!echo: Returns the input  
- usage: !echo arg1 arg2  
- arg1: int  
- arg2: string  
- example: !echo 5 "Hello World"  

!votemute: Initiates a vote, where users can reply with "yes" or "no".  
            All votes are stored in a dictionary and voters in a list.  
            Only allows one voting session to run at a time, and only collects  
            unique votes.  
- usage: !votemute arg1  
- arg1: string, Discord mention)  
- example: !votemute @JohnDoe#1234  

!voteunmute: Initiates a vote, where users can reply with "yes" or "no".   
            All votes are stored in a dictionary and voters in a list,  
            only allows one voting session to run at a time, and only collects  
            unique votes.  
- usage: !voteunmute arg1  
- arg1(string, Discord mention)  
- example: !voteunmute @JohnDoe#1234  

!giverole: Gives the user a role with default permissions  
- usage: !giverole arg1 arg2  
- arg1: string  
- arg2: hexadecimal  
- example: !giverole "black" #000000  
  
!removerole: Removes a role from the user  
- usage: !removerole arg1  
- arg1: string  
- example: !removerole "black"  

!wordcloud: generates a wordcloud from the last 5000 messages sent in the server  
             these messages are retreived from the built in cache of the bot,  
             restarting the bot or a crash will clear this cache!  
- example: !wordcloud  

!emoji: Returns the input text replaced with emojis  
- usage: !emoji arg1  
- arg1: string  
- example: !emoji "I want 10 apples"  

!wolfram: Returns the result from wolframalpha based on client input  
- usage: !wolfram arg1   
- arg1: string  
- example: !wolfram "what is the temperature of the sun"  

!wolfram_image: Returns the result as an image from wolframalpha based on client input  
- usage: !wolfram_image arg1   
- arg1: string  
- example: !wolfram_image "graph of y=x^2"  
  
!google: Returns a random google image from the top 5 results based on keywords  
- usage: !google arg1  
- arg1: string  
- example: !google "street car"  

!youtube: Plays the audio from a YouTube video  
- usage: !youtube arg1  
- arg1: string  
- example: !youtube "https://www.youtube.com/watch?v=_4IRMYuE1hI"  

!disconnect: Disconnects the bot from a voice channel  
- usage: !disconnect  
- arg1: string  

!flip: Returns heads or tails, emulates a coin flip  
- usage: !flip  

!copypasta: Saves the input text to a text file, to be recalled later  
- usage: !copypasta arg1 arg2  
- arg1: string  
- arg2: string  
- example: !copypasta "python" "Python is a great programming language"  

!pasta: Returns the text saved with !copypasta  
- usage: !pasta arg1  
- arg1: string  
- example: !pasta "python"  

!oof: Plays the audio from /sounds/oof.m4a   
- usage: !youtube arg1  
- arg1: string  
- example: !youtube "https://www.youtube.com/watch?v=_4IRMYuE1hI"  

!meme clown: Returns an image with text added from the user input  
- usage: !meme clown arg1  
- arg1: string  
- example: !meme clown "funny generic text"  