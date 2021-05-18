""" botchan
the main program for the discord bot """

# import data libraries
import json
import yaml
import dotenv

# import discord extension commands
from discord.ext import commands

# import custom cogs
from cogs.schedule import Schedule
from cogs.maintain import Maintain
from cogs.provide import Provide

# import custom anilist api wrapper
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
    """ primary function that runs the bot """

    # set up environmental variables
    config = dotenv.dotenv_values('.env')

    # bot token that is required to log into the correct bot
    bot_token = config['BOT_TOKEN']

    # set up anilist api
    anilist_api = AniList()

    # set up emojis
    emojis = load_emojis('data/emojis.yml')

    # set up the command prefix
    bot = commands.Bot(command_prefix='$weeb')

    # set up the custom cogs
    bot.add_cog(Schedule(bot, anilist_api, emojis, config))
    bot.add_cog(Maintain(bot, anilist_api, emojis, config))
    bot.add_cog(Provide(bot, anilist_api, emojis, config))

    # run the bot
    bot.run(bot_token)

if __name__ == '__main__':
    main()