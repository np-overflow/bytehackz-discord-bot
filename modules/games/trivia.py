from typing import Type
from dis_snek.models import Scale
from dis_snek.models.application_commands import (
    OptionTypes,
    slash_command,
    slash_option,
)
from dis_snek.models.context import InteractionContext
from dis_snek.models.discord_objects.embed import EmbedAttachment
from dis_snek.models.discord_objects.embed import Embed
from dis_snek.models.context import InteractionContext
from dis_snek.models.discord_objects.embed import EmbedAttachment, EmbedField
from dis_snek.models.discord_objects.components import Button, ActionRow
from dis_snek.models.discord_objects.channel import GuildText, PermissionOverwrite
from dis_snek.models.discord_objects.guild import Guild
from dis_snek.models.enums import ButtonStyles
from dis_snek.models.discord_objects.embed import Embed
from dis_snek.models.listener import listen
from dis_snek.http_requests.channels import ChannelRequests

import requests
import json
import random 

class Trivia(Scale):
    def __init__(self, bot):
        self.bot = bot
        self.data = self.get_API()




    def get_API():
        response_api= requests.get('https://opentdb.com/api.php?amount=50&category=15&difficulty=medium&type=multiple')
        data = response_api.text
        parse_json = json.loads(data)   
        return parse_json

    @slash_command("start_game", "Start a game of Trivia Questions!")
    @slash_option(
        "queuechannel",
        "ChannelID of channel to set up queue",
        OptionTypes.CHANNEL,
        required=True,
    )
    async def start_game(self, ctx: InteractionContext, queuechannel, boardchannel):

        if type(queuechannel) != GuildText or type(boardchannel) != GuildText:
            await ctx.send(
                embeds=[
                    Embed("Whoops", f"Channels must be text channels", color="#F9AC42")
                ]
            )
            return

        await queuechannel.purge()

        embed = Embed(
            "Room Of Trivia",
            "Think you can beat my knowledge on video games? Well think again \n \
             You're going down! ",
        )
        await queuechannel.send(embeds=[embed])
        ''' 
        rng = random.randint(0,50)
        qns_object = self.data['results'][rng]
        lst_of_choices = qns_object["incorrect_answers"]
        lst_of_choices.append(qns_object["correct_answer"])
        choice1 = random.choice(lst_of_choices)
        lst_of_choices.remove(choice1)
        choice2 = random.choice(lst_of_choices)
        lst_of_choices.remove(choice2)
        choice3 = random.choice(lst_of_choices)
        lst_of_choices.remove(choice3)
        choice4 = random.choice(lst_of_choices)
        lst_of_choices.remove(choice4)
        '''
        '''
        if choice =="1":
            if choice1 == qns_object["correct_answer"]:
                print("Correct")
            else:
                print("wrong") 
        elif choice =="2":
            if choice2 == qns_object["correct_answer"]:
                print("Correct")
            else:
                print("wrong") 
        elif choice =="3":
            if choice3 == qns_object["correct_answer"]:
                print("Correct")
            else:
                print("wrong") 
        elif choice=="4":
            if choice4 == qns_object["correct_answer"]:
                print("Correct")
            else:
                print("wrong") 
        else:
            print("Invalid choice please try again!")
        '''
        button1 = Button(
            style=ButtonStyles.BLURPLE, 
            label="Play Trivia", emoji="▶",
            custom_id="getIn" #Camel case good, dont @ me

        )
        await queuechannel.send(
            "Challenge me",
            components=[button1]
        )


        

def setup(bot):
    Trivia(bot)
