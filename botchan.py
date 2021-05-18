""" botchan
the main program for the discord bot """

import json
import yaml
import random
import dotenv
import discord
from discord.ext import commands

from cogs.schedule import Schedule
from cogs.maintain import Maintain
from cogs.provide import Provide

# import anilist api wrapper
from api.anilist import AniList

def load_emojis(filename):
    """ load emojis
    simple function to load the emojis datastructure """

    # initialize emojis
    emojis = {}

    # load the emojis
    with open(filename, 'r') as fn:
        emojis = yaml.load(fn, Loader=yaml.FullLoader)

    return emojis

def main():
    # set up environmental variables
    config = dotenv.dotenv_values('.env')

    # bot token that is required to log into the correct bot
    bot_token = config['BOT_TOKEN']

    # primary channel id for the bot to post messages to
    channel_id = config['CHANNEL_ID']

    # primary role id for the bot to mention in messages
    role_id = config['ROLE_ID']

    # set up icon url for embeds
    icon_url = config['ICON_URL']

    # set up anilist user
    anilist_user = config['ANILIST_USER']

    # set up anilist api
    anilist_api = AniList()

    # set up emojis
    emojis = load_emojis('data/emojis.yml')

    # set up the command prefix
    bot = commands.Bot(command_prefix='$weeb')
    bot.add_cog(Schedule(bot, anilist_api, emojis, channel_id, role_id))
    bot.add_cog(Maintain(bot, anilist_api, emojis))
    bot.add_cog(Provide(bot, anilist_api, icon_url, anilist_user))

    # run the bot
    bot.run(bot_token)

if __name__ == '__main__':
    main()