"""
Discord Rikka Bot.
Carlos Saucedo, 2018
"""

import discord
import asyncio
import gizoogle
from random import randint
import string
from googletrans import Translator
import dbl

#Auth tokens
tokenfile = open("auth_token.txt", "r")
rawtoken = tokenfile.read().splitlines()
token = rawtoken[0]

bltokenfile = open("dbl_token.txt", "r")
rawbltoken = bltokenfile.read().splitlines()
bltoken = rawbltoken[0]
shardCount = 1 #Keeping it simple with 1 for now.

#lists
hugsfile = open("hug_gifs.list", "r")
huglist = hugsfile.read().splitlines()
hugcount = len(huglist) - 1 # -1 to compensate for array lengths.
ramsayfile = open("ramsay.list")
ramsaylist = ramsayfile.read().splitlines()
ramsayCount = len(ramsaylist) - 1
insultfile = open("InsultGenerator")
insultlist = insultfile.read().splitlines()
insultCount = len(ramsaylist) - 1

#Prefix file accessing

#Instances
client = discord.Client()
translator = Translator()
botlist = dbl.Client(client, bltoken)

#Prefix things
defaultPrefix = ";"
        

def getServerPrefix(server):
    #Returns the server prefix.
    #If there is no server prefix set, it returns the defaultPrefix.
    prefixFile = open("server_prefixes.txt", "r+")
    prefixList = prefixFile.read().splitlines()
    prefixFile.close()
    serverInList = False
    for line in prefixList:
        splitLine = line.split()
        if server.id == splitLine[0]:
            serverInList = True
            return splitLine[1]
    if serverInList == False:
        #If server does not have default prefix set
        return defaultPrefix

def command(string, message):
    #Builds a command out of the given string.
    serverPrefix = getServerPrefix(message.server)
    return serverPrefix + string

def getArgument(command, message):
    #Gets the argument text as a string.
    argument = message.content.replace(command + " ", "")
    argument = argument.encode("ascii", "ignore")
    return argument

def getRawArgument(command, message):
    argument = message.content.replace(command + " ", "")
    return argument
    
@client.event
async def on_server_join(server):
    serversConnected = str(len(client.servers))
    print("Joined server " + server.name + "!")
    print("Guilds connected: " + serversConnected)#Returns number of guilds connected to
    await client.change_presence(game=discord.Game(name='on ' + serversConnected + ' servers!'))
    try:
        await botlist.post_server_count(serversConnected, shardCount)
        print("Successfully published server count to dbl.")
    except Exception as e:
        print("Failed to post server count to tbl.")
    
@client.event
async def on_server_remove(server):
    serversConnected = str(len(client.servers))
    print("Left server " + server.name + "!")
    print("Guilds connected: " + serversConnected)#Returns number of guilds connected to
    await client.change_presence(game=discord.Game(name='on ' + serversConnected + ' servers!'))
    try:
        await botlist.post_server_count(serversConnected, shardCount)
        print("Successfully published server count to dbl.")
    except Exception as e:
        print("Failed to post server count to tbl.") 
    
@client.event
async def on_message(message):
    """
    Universal commands
    """
    
    if message.author == client.user:
        #Makes sure bot does not reply to itself
        return
    
    if message.author.bot == True:
        #Makes sure bot does not reply to another bot.
        return
    
    if message.content.startswith(command("help", message)):
        #Returns the README on the GitHub.
        msg = "{0.author.mention} https://discordbots.org/bot/430482288053059584".format(message)
        await client.send_message(message.channel, msg)
    
    if message.content.startswith(command("hello", message)) or message.content.startswith(command("hi", message)):
        #Says hi and embeds a gif, mentioning the author of the message.
        msg = "h-hello {0.author.mention}-chan! ".format(message) + 'https://cdn.discordapp.com/attachments/402744318013603840/430592483282386974/image.gif'
        await client.send_message(message.channel, msg)
    
    if message.content.startswith(command("gizoogle", message)):
        #Gizoogles the given string and returns it.
        translatedMessage = gizoogle.text(getArgument(command("gizoogle", message), message))
        msg = "{0.author.mention} says: ".format(message) + translatedMessage.format(message)
        await client.send_message(message.channel, msg)
        await client.delete_message(message)
    
    if message.content.startswith(command("hugme", message)) or message.content == command("hug", message):
        #Hugs the author of the message.
        msg = "{0.author.mention}: ".format(message) + huglist[randint(0,hugcount)] 
        await client.send_message(message.channel, msg)
    
    if message.content.startswith(command("hug ", message)):
        #Hugs the first user mentioned by the author.
        msg = "{0.author.mention} hugs {0.mentions[0].mention}! ".format(message) + huglist[randint(0,hugcount)]
        await client.send_message(message.channel, msg)
        await client.delete_message(message)
        
    if message.content.startswith(command("ramsay", message)):
        #Replies with a random Gordon Ramsay quote.
        msg = ramsaylist[randint(0, ramsayCount)]
        await client.send_message(message.channel, msg)
        
    if message.content.startswith(command("insult ", message)):
        #Says a random insult using an insult generator
        msg = "{0.author.mention} calls {0.mentions[0].mention} a " + insultlist[randint(0, insultCount)]
        await client.send_message(message.channel, msg)
        await client.delete_message(message)
    
    if message.content.startswith(command("gay", message)):
        #no u
        msg = "no u {0.author.mention}".format(message)
        await client.send_message(message.channel, msg)

    if message.content.startswith(command("translate", message)):
        #Translates the given text into english.
        translatedMessage = translator.translate(getRawArgument(command("translate", message), message)).text
        msg = ("{0.author.mention}: translated text - " + translatedMessage).format(message)
        await client.send_message(message.channel, msg)
        
    if message.content.startswith(command("info", message)):
        #Returns information about the bot.
        msg = ("Hi there! I'm Rikka. This robot was created by Leo. This server's command Prefix is: " + getServerPrefix(message.server) + ". To get help, use " + getServerPrefix(message.server) + "help.").format(message)
        await client.send_message(message.channel, msg)
        
    if (len(message.mentions) > 0) and (message.mentions[0] == client.user) and ("help" in message.content):
        #Returns information about the bot.
        msg = ("Hi there! I'm Rikka. This robot was created by Leo. This server's command Prefix is: " + getServerPrefix(message.server) + ". To get help, use " + getServerPrefix(message.server) + "help.").format(message)
        await client.send_message(message.channel, msg)

    """
    Administrator Commands.
    """
    if message.channel.permissions_for(message.author).administrator == True:
        if message.content.startswith(command("clear", message)):
            #Removes a set number of messages.
            number = int(getArgument(command("clear", message), message)) + 2
            counter = 0
            async for x in client.logs_from(message.channel, limit=number):
                if counter < number :
                    await client.delete_message(x)
                    counter += 1
                    await asyncio.sleep(0.1)
            msg = "deleted " + str(number - 2) + " messages!".format(string)
            await client.send_message(message.channel, msg)

        if message.content.startswith(command("prefix", message)):
            #Changes the prefix to the specified string.
            prefixFile = open("server_prefixes.txt")
            prefixList = prefixFile.read().splitlines()
            prefixFile.close()
            serverInList = False #Gotta initialize the variable
            newPrefix = getRawArgument(command("prefix", message), message)
            index = 0
            for line in prefixList:
                splitLine = line.split()
                if(message.server.id == splitLine[0]):
                    #If the server already has a custom prefix set
                    serverInList = True
                    prefixFile = open("server_prefixes.txt", "w+")
                    prefixList[index] = (message.server.id + " " + newPrefix)
                    prefixFile.write("\n".join(prefixList))
                    prefixFile.close()
                    msg = ("Changed server prefix to " + newPrefix + " !").format(message)
                    await client.send_message(message.channel, msg)
                index = index + 1
            if serverInList == False:
                #If the server does not already have a custom prefix set
                prefixFile = open("server_prefixes.txt", "a+")
                prefixFile.write(message.server.id + " " + newPrefix+"\n") #Adds line to prefixlist
                prefixFile.close()
                msg = ("Set server prefix to " + newPrefix + " !").format(message)
                await client.send_message(message.channel, msg)
    """
    Miscellaneous gifs.
    I know it's ugly, but I'll fix it eventually.
    """
    #Rikka's actions
    if message.content == command("shocked", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430591612637413389/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("smile", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430591877834735617/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("hentai", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430593080215994370/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("blush", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430593551554969600/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("bdsm", message):
        msg = "http://i.imgur.com/dI4zJwk.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("rekt", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430594037427470336/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("boop", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430594711602987008/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("fuckoff", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430594846022041601/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("sanic", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430595068156575756/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("dreamy", message):
        msg = "https://cdn.discordapp.com/attachments/402744318013603840/430595392669745153/image.gif"
        await client.send_message(message.channel, msg)
    if message.content == command("waifu", message):
        msg = "https://i.pinimg.com/originals/bd/9a/a4/bd9aa46572e180ec6df08119429a1e81.jpg"
        await client.send_message(message.channel, msg)
    if message.content == command("trash", message):
        msg = "https://media1.tenor.com/images/29307201260fb755e7ff9fec21f22c95/tenor.gif?itemid=8811727"
        await client.send_message(message.channel, msg)
    if message.content == command("kys", message):
        msg = "https://imgur.com/YfYwzcN"
        await client.send_message(message.channel, msg)
    #SyCW Commands - By special request.
    if message.server.id == "329383300848418816":
        if message.content == command("assad", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430787413888073728/image.jpg"
            await client.send_message(message.channel, msg)
        if message.content == command("turkey", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430787599343550494/image.jpg"
            await client.send_message(message.channel, msg)
        if message.content == command("bomb", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430787955880230912/image.jpg"
            await client.send_message(message.channel, msg)
        if message.content == command("isis", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430788102399983617/image.png"
            await client.send_message(message.channel, msg)
        if message.content == command("barrel", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430788296663367680/image.jpg"
            await client.send_message(message.channel, msg)
        if message.content == command("kurd", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430789263945105412/image.jpg"
            await client.send_message(message.channel, msg)
        if message.content == command("abuhajaar", message):
            msg = "https://cdn.discordapp.com/attachments/422581776247029761/430804463016476672/image.png"
            await client.send_message(message.channel, msg)
        
"""
Bot login actions
"""
@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("-------")
    print("loaded hugs: " + str(hugcount + 1)) # +1 because humans are not computers.
    print("loaded Ramsay quotes: " + str(ramsayCount + 1))
    serversConnected = str(len(client.servers))
    print("Guilds connected: " + serversConnected)#Returns number of guilds connected to
    await client.change_presence(game=discord.Game(name='on ' + serversConnected + ' servers!'))
    try:
        await botlist.post_server_count(serversConnected, shardCount)
        print("Successfully published server count to dbl.")
    except Exception as e:
        print("Failed to post server count to tbl.")
