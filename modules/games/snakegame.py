from typing import Type
from dis_snek.models import Scale, User, listen
from dis_snek.models.application_commands import (
    OptionTypes,
    slash_command,
    slash_option,
)
from dis_snek.models.command import message_command
from dis_snek.models.context import InteractionContext
from dis_snek.models.discord_objects.embed import EmbedAttachment
from dis_snek.models.discord_objects.embed import Embed

import os
import numpy as np
import random


class SnakeGame(Scale):
    def __init__(self, bot):
        self.bot = bot
    
    @slash_command("snakes", "Let's Play")
    async def blame(self, ctx: InteractionContext):
        embed = Embed(
            "XD",
            color="#F9AC42",
            image="https://cdn.discordapp.com/attachments/903207401623281676/903895467522408458/blame.png",
        )

        await ctx.send(embeds=[embed])

    # await channel.send('hello')
    @listen()
    async def on_message_create(self, event):
        return
        message = event.message
        # print("Message Channel : {}".format(message.channel))
        # print(os.environ['CHANNEL_ID'])
        gameChannel = message.channel
        # print("gameChannel Channel : {}".format(gameChannel))
        if(message.author.id == self.bot.user.id):
                return
        if gameChannel == message.channel:
            if(message.content.startswith('!hello')):
                # print(message.channel)
                reset()
                embedVar = getNormalEmbededData(title="Welcome *{0.author}* to our Useless Game Channel ! Lets Play Game".format(message), description="⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜\n⬜⬛⬛⬛⬛⬛⬛⬛🍎⬛⬜\n⬜⬛🟨🟨⬛⬛⬛⬛⬛⬛⬜\n⬜⬛⬛🟨🟨🟨🟨⬛⬛⬛⬜\n⬜⬛⬛⬛⬛⬛🟨🟨⬛⬛⬜\n⬜⬛⬛⬛⬛⬛⬛🟨🟨😵⬜\n⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜\n⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜\n⬜⬛⬛⬛⬛⬛⬛⬛⬛⬛⬜\n⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜\n\n` a ` -> Move Left\n` d ` -> Move Right\n` w ` -> Move Up\n` s ` -> Move Down\n` r ` -> Reset")
                await message.channel.send(embeds=embedVar)
            elif(message.content.startswith('r')):
                print("Reset")
                reset()
                embedVar=getNormalEmbededData(title="Pick Apple Game", description="{}\nGame has been reset. You can start playing new game".format(getGameGrid()))
                embedVar.add_field(name="Your Score", value=str(points), inline=True)
                await message.channel.send(embeds=embedVar)
            elif(isOut):
                embedVar=getErrorEmbededData(title="Game Over", description="Scored Point : {}".format(points))
                await message.channel.send(embeds=embedVar)
            elif(message.content.startswith('w')):
                moveUp()
                await sendMessage(message)
            elif(message.content.startswith('a')):
                moveLeft()
                await sendMessage(message)
            elif(message.content.startswith('s')):
                moveDown()
                await sendMessage(message)
            elif(message.content.startswith('d')):
                moveRight()
                await sendMessage(message)
            else:
                embedVar = getErrorEmbededData(title="*Error*", description="Invalid Input Detected ! Please enter a valid input. \n ` a ` -> Move Left\n` d ` -> Move Right\n` w ` -> Move Up\n` s ` -> Move Down\n` r ` -> Reset")
                await message.channel.send(embeds=embedVar)
        else:
            print("Wrong Channel")
            
    @message_command(name='test')
    async def check(self, ctx):
        if ctx.channel.name == 'game':
            await ctx.send("Response message")


wall = "⬜"
innerWall = "⬛"
energy = "🍎"
snakeHead = "😍"
snakeBody = "🟨"
snakeLoose = "😵"


def getGameGrid():
    str = ""

    for item in snakeMatrix:
        # print(item)
        for i in item:
            if(i == 0):
                str += wall
            elif i == 1:
                str += innerWall
            elif i == 2:
                str += snakeHead
            elif i == 3:
                str += snakeBody
            elif i == 4:
                str += energy
            else:
                str += snakeLoose
        str += "\n"
        
    return str

def generateRandomEnergy():
    snakeMatrix[random.randint(1,10)][random.randint(1,10)] = 4

def checkEnergy(i, j):
    # print("i : {}".format(i))
    # print("j : {}".format(j))
    # print("Pos Val : {}".format(snakeMatrix[i][j]))
    return snakeMatrix[i][j] == 4

def handleEnergy(i, j):
    global points
    # print(checkEnergy(i, j))
    if(checkEnergy(i, j)):
        generateRandomEnergy()
        points += 1

def updateSnakePosition(i, j, k, l):
    snakeMatrix[i][j] = 2
    snakeMatrix[k][l] = 1

def isOuterBoundary(i, j):
    global isOut
    if(i == 0 or j == 0 or i == 11 or j == 11):
        # print("Out")
        snakeHeadPos = np.argwhere(snakeMatrix == 2)[0]
        snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]] = 5
        isOut = True
        print("isOut : {}".format(isOut))
        return True
    return False

def moveUp():
    # print("Up")
    snakeHeadPos = np.argwhere(snakeMatrix == 2)[0]
    # print(snakeHeadPos)
    # print(snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]])
    if(not isOuterBoundary(snakeHeadPos[0]-1, snakeHeadPos[1])):
        handleEnergy(snakeHeadPos[0]-1, snakeHeadPos[1])
        updateSnakePosition(snakeHeadPos[0]-1, snakeHeadPos[1], snakeHeadPos[0], snakeHeadPos[1])
    # snakeMatrix[snakeHeadPos[0]-1][snakeHeadPos[1]] = 2
    # snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]] = 1


def moveLeft():
    # print("Left")
    snakeHeadPos = np.argwhere(snakeMatrix == 2)[0]
    if(not isOuterBoundary(snakeHeadPos[0], snakeHeadPos[1]-1)):
        handleEnergy(snakeHeadPos[0], snakeHeadPos[1]-1)
        updateSnakePosition(snakeHeadPos[0], snakeHeadPos[1]-1, snakeHeadPos[0], snakeHeadPos[1])
    # snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]-1] = 2
    # snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]] = 1


def moveRight():
    # print("Right")
    snakeHeadPos = np.argwhere(snakeMatrix == 2)[0]
    if(not isOuterBoundary(snakeHeadPos[0], snakeHeadPos[1]+1)):
        handleEnergy(snakeHeadPos[0], snakeHeadPos[1]+1)
        updateSnakePosition(snakeHeadPos[0], snakeHeadPos[1] + 1, snakeHeadPos[0], snakeHeadPos[1])
    # snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]+1] = 2
    # snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]] = 1


def moveDown():
    # print("Down")
    snakeHeadPos = np.argwhere(snakeMatrix == 2)[0]
    if(not isOuterBoundary(snakeHeadPos[0]+1, snakeHeadPos[1])):
        handleEnergy(snakeHeadPos[0]+1, snakeHeadPos[1])
        updateSnakePosition(snakeHeadPos[0]+1, snakeHeadPos[1], snakeHeadPos[0], snakeHeadPos[1])
    # snakeMatrix[snakeHeadPos[0]+1][snakeHeadPos[1]] = 2
    # snakeMatrix[snakeHeadPos[0]][snakeHeadPos[1]] = 1

def reset():
    global snakeMatrix, isOut, points
    isOut = False
    # print("Reset")
    snakeMatrix = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    points = 0
    generateRandomEnergy()

def getNormalEmbededData(title, description):
    return Embed(title=title, description=description)

def getErrorEmbededData(title, description):
    return Embed(title=title, description=description)


async def sendMessage(message):
    embedVar=getNormalEmbededData(title="Pick Apple Game", description="{}".format(getGameGrid()))
    embedVar.add_field(name="Your Score", value=str(points), inline=True)
    await message.channel.send(embeds=embedVar)

#client = discord.Client()

points = 0
isOut = False
snakeMatrix = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
generateRandomEnergy()

def setup(bot):
    SnakeGame(bot)
    