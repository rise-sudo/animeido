""" botchan
the main program for the discord bot """

import json
import dotenv
import aiocron
import discord
from discord.ext import commands

# import anilist api wrapper
from api.anilist import AniList

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

# all available emojis
happy_emoji_1_id = int(config['HAPPY_EMOJI_1_ID'])
happy_emoji_2_id = int(config['HAPPY_EMOJI_2_ID'])
happy_emoji_3_id = int(config['HAPPY_EMOJI_3_ID'])
happy_emoji_4_id = int(config['HAPPY_EMOJI_4_ID'])
happy_emoji_5_id = int(config['HAPPY_EMOJI_5_ID'])
happy_emoji_6_id = int(config['HAPPY_EMOJI_6_ID'])
shock_emoji_1_id = int(config['SHOCK_EMOJI_1_ID'])
shock_emoji_2_id = int(config['SHOCK_EMOJI_2_ID'])
shock_emoji_3_id = int(config['SHOCK_EMOJI_3_ID'])

# set up the command prefix
bot = commands.Bot(command_prefix='$weeb')

# set up anilist api
anilist_api = AniList()

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

@bot.command()
async def add(ctx, anilist_url):
    """ provide anilist url to add to PTW list """

    # add to the existing anilist
    result = anilist_api.add(anilist_url)

    # build emojis
    happy_emoji = bot.get_emoji(happy_emoji_1_id)
    shock_emoji = bot.get_emoji(shock_emoji_1_id)

    # respond to the user depending on the attempt
    if result:
        usr_msg = "かしこまりました、ご主人様。"
        usr_msg += "\nI have successfully updated anilist!"
        await ctx.send(usr_msg)
        await ctx.send(happy_emoji)
    else:
        usr_msg = "申し訳ありません、ご主人様！！"
        usr_msg += "\nI was unable to process your command!"
        await ctx.send(usr_msg)
        await ctx.send(shock_emoji)

@bot.command()
async def update(ctx, anilist_url, progress):
    """ provide an anilist url and episode progress (e.g. +2, -4, 7) """

    # update anilist with the episode count
    result = anilist_api.update(anilist_url, progress=progress)
    title = anilist_api.get_title(anilist_url)

    # build emojis
    happy_emoji = bot.get_emoji(happy_emoji_2_id)
    shock_emoji = bot.get_emoji(shock_emoji_2_id)

    # respond to the user depending on the attempt
    if result:
        previous_progress = result[0]
        current_progress = result[1]
        usr_msg = "かしこまりました、ご主人様。"
        usr_msg += "\nI have successfully updated anilist!"
        usr_msg += f"\n{title}: {previous_progress} --> {current_progress}"
        await ctx.send(usr_msg)
        await ctx.send(happy_emoji)
    else:
        usr_msg = "申し訳ありません、ご主人様！！"
        usr_msg += "\nI was unable to process your command!"
        await ctx.send(usr_msg)
        await ctx.send(shock_emoji)

@bot.command()
async def rate(ctx, anilist_url, score):
    """ provide an anilist url and a score to rate an anime """

    # update anilist with the rating
    result = anilist_api.rate(anilist_url, score=score)
    title = anilist_api.get_title(anilist_url)

    # build emojis
    happy_emoji = bot.get_emoji(happy_emoji_3_id)
    shock_emoji = bot.get_emoji(shock_emoji_3_id)

    # respond to the user depending on the attempt
    if result:
        usr_msg = "かしこまりました、ご主人様。"
        usr_msg += "\nI have successfully updated anilist!"
        await ctx.send(usr_msg)
        await ctx.send(happy_emoji)
    else:
        usr_msg = "申し訳ありません、ご主人様！！"
        usr_msg += "\nI was unable to process your command!"
        await ctx.send(usr_msg)
        await ctx.send(shock_emoji)

@bot.command()
async def schedule(ctx, anilist_url_1, anilist_url_2, anilist_url_3):
    """ schedules the three anime sessions - must provide 3 anilist urls """

    # build emojis
    happy_emoji = bot.get_emoji(happy_emoji_4_id)

    # build a dictionary for the scheduled anime
    schedule = {
        'anime_1': anilist_url_1,
        'anime_2': anilist_url_2,
        'anime_3': anilist_url_3,
    }

    # dump it to a temporary file
    with open('schedule.json', 'w') as fn:
        json.dump(schedule, fn)

    usr_msg = "かしこまりました、ご主人様。"
    usr_msg += "\nI have successfully updated the scheduled messages!"
    await ctx.send(usr_msg)
    await ctx.send(happy_emoji)

@aiocron.crontab('0 17 * * 0')
async def sunday_message():
    """ sunday scheduled message """

    # set up the channel to post in
    channel = bot.get_channel(int(channel_id))

    # build emojis
    happy_emoji = bot.get_emoji(happy_emoji_5_id)

    # load the requested scheduled anime
    schedule = {}
    with open('schedule.json', 'r') as fn:
        schedule = json.load(fn)

    # set up the anime urls
    anime_1_url = schedule.get('anime_1', '')
    anime_2_url = schedule.get('anime_2', '')

    # set up the titles
    anime_1_title = anilist_api.get_title(anime_1_url)
    anime_2_title = anilist_api.get_title(anime_2_url)

    # set up the progress
    anime_1_progress = anilist_api.get_current_progress(anime_1_url)
    anime_2_progress = anilist_api.get_current_progress(anime_2_url)

    # set up the message to the user
    usr_msg = f'<@&{role_id}> おはようございます、ご主人様たち！'
    usr_msg += '\nWe have the following anime scheduled for today.'
    usr_msg += f'\n  **2:00 PM PST**: {anime_1_title}. Currently on episode {anime_1_progress}.'
    usr_msg += f'\n  **7:30 PM PST**: {anime_2_title}. Currently on episode {anime_2_progress}.'
    usr_msg += f'\nHope to see you there!'

    await channel.send(usr_msg)
    await channel.send(happy_emoji)

@aiocron.crontab('0 17 * * 1')
async def monday_message():
    """ monday scheduled message """

    # set up the channel to post in
    channel = bot.get_channel(int(channel_id))

    # build emojis
    happy_emoji = bot.get_emoji(happy_emoji_6_id)

    # load the requested scheduled anime
    schedule = {}
    with open('schedule.json', 'r') as fn:
        schedule = json.load(fn)

    # set up the anime urls
    anime_3_url = schedule.get('anime_3', '')

    # set up the titles
    anime_3_title = anilist_api.get_title(anime_3_url)

    # set up the progress
    anime_3_progress = anilist_api.get_current_progress(anime_3_url)

    # set up the message to the user
    usr_msg = f'<@&{role_id}> おはようございます、ご主人様たち！'
    usr_msg += '\nWe have the following anime scheduled for today.'
    usr_msg += f'\n  **7:30 PM PST**: {anime_3_title}. Currently on episode {anime_3_progress}.'
    usr_msg += f'\nHope to see you there!'

    await channel.send(usr_msg)
    await channel.send(happy_emoji)

# run the bot
bot.run(bot_token)