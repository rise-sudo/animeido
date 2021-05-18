""" botchan
the main program for the discord bot """

import json
import yaml
import random
import dotenv
import aiocron
import discord
from discord.ext import commands

from cogs.schedule import Schedule
from cogs.maintain import Maintain

# import anilist api wrapper
from api.anilist import AniList

# load the emojis
with open('data/emojis.yml', 'r') as fn:
    emojis = yaml.load(fn, Loader=yaml.FullLoader)

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

# set up the command prefix
bot = commands.Bot(command_prefix='$weeb')
bot.add_cog(Schedule(bot, anilist_api, emojis, channel_id, role_id))
bot.add_cog(Maintain(bot, anilist_api, emojis))

@bot.event
async def on_ready():
    """ on ready
    generates a message once the bot has successfully logged into discord """

    # print to the console screen
    print(f'Logged in as {bot.user.name} with id of {bot.user.id}.')
    print('------')

@bot.command()
async def search(ctx, *search_term: str):
    """ search with any term or terms """

    # search via the anilist api and get the url results
    anilist_urls = anilist_api.search(' '.join(search_term))

    # set up embed
    embed = discord.Embed(
        title="AniList Search",
        color=0xaaa9ad,
        description=f"Found {len(anilist_urls)} matches!"
    )
    embed.set_author(
        name="アニメイド", 
        icon_url=icon_url, 
        url=f"https://anilist.co/user/{anilist_user}/"
    )
    embed.set_thumbnail(url=icon_url)

    # iterate through the urls and send to user
    for anilist_url in anilist_urls:
        title = anilist_url[0]
        url = anilist_url[1]
        embed.add_field(name=title, value=url, inline=False)
        
    await ctx.send(embed=embed)
# run the bot
bot.run(bot_token)