""" schedule
cog that handles all scheduling tasks
which includes announcements for members """

from discord.ext import commands
import random
import json
import aiocron

class Schedule(commands.Cog):
    def __init__(self, bot, anilist_api, emojis, channel_id, role_id):
        self.bot = bot
        self.anilist_api = anilist_api
        self.emojis = emojis
        self.channel_id = channel_id
        self.role_id = role_id

        @aiocron.crontab('0 17 * * 0')
        async def on_monday_reminder():
            await self.sunday_message()

        @aiocron.crontab('0 17 * * 1')
        async def on_sunday_reminder():
            await self.monday_message()

    @commands.command()
    async def schedule(self, ctx, anilist_url_1, anilist_url_2, anilist_url_3):
        """ schedules the three anime sessions - must provide 3 anilist urls """

        # build emojis
        positive_emoji = self.bot.get_emoji(random.choice(self.emojis['positive']))

        # build a dictionary for the scheduled anime
        schedule = {
            'anime_1': anilist_url_1,
            'anime_2': anilist_url_2,
            'anime_3': anilist_url_3,
        }

        # dump it to a temporary file
        with open('data/schedule.json', 'w') as fn:
            json.dump(schedule, fn)

        usr_msg = "かしこまりました、ご主人様。"
        usr_msg += "\nI have successfully updated the scheduled messages!"
        await ctx.send(usr_msg)
        await ctx.send(positive_emoji)

    async def sunday_message(self):
        """ sunday scheduled message """

        # set up the channel to post in
        channel = self.bot.get_channel(int(self.channel_id))

        # build emojis
        positive_emoji = self.bot.get_emoji(random.choice(self.emojis['positive']))

        # load the requested scheduled anime
        schedule = {}
        with open('data/schedule.json', 'r') as fn:
            schedule = json.load(fn)

        # set up the anime urls
        anime_1_url = schedule.get('anime_1', '')
        anime_2_url = schedule.get('anime_2', '')

        # set up the titles
        anime_1_title = self.anilist_api.get_title(anime_1_url)
        anime_2_title = self.anilist_api.get_title(anime_2_url)

        # set up the progress
        anime_1_progress = self.anilist_api.get_current_progress(anime_1_url)
        anime_2_progress = self.anilist_api.get_current_progress(anime_2_url)

        # set up the message to the user
        usr_msg = f'<@&{self.role_id}> おはようございます、ご主人様たち！'
        usr_msg += '\nWe have the following anime scheduled for today.'
        usr_msg += f'\n  **2:00 PM PST**: {anime_1_title}. Currently on episode {anime_1_progress}.'
        usr_msg += f'\n  **7:30 PM PST**: {anime_2_title}. Currently on episode {anime_2_progress}.'
        usr_msg += f'\nHope to see you there!'

        await channel.send(usr_msg)
        await channel.send(positive_emoji)
 
    async def monday_message(self):
        """ monday scheduled message """

        # set up the channel to post in
        channel = self.bot.get_channel(int(self.channel_id))

        # build emojis
        positive_emoji = self.bot.get_emoji(random.choice(self.emojis['positive']))

        # load the requested scheduled anime
        schedule = {}
        with open('data/schedule.json', 'r') as fn:
            schedule = json.load(fn)

        # set up the anime urls
        anime_3_url = schedule.get('anime_3', '')

        # set up the titles
        anime_3_title = self.anilist_api.get_title(anime_3_url)

        # set up the progress
        anime_3_progress = self.anilist_api.get_current_progress(anime_3_url)

        # set up the message to the user
        usr_msg = f'<@&{self.role_id}> おはようございます、ご主人様たち！'
        usr_msg += '\nWe have the following anime scheduled for today.'
        usr_msg += f'\n  **7:30 PM PST**: {anime_3_title}. Currently on episode {anime_3_progress}.'
        usr_msg += f'\nHope to see you there!'

        await channel.send(usr_msg)
        await channel.send(positive_emoji)