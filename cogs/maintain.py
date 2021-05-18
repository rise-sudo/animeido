""" maintain
cog that handles all maintaining anilist profile """

from discord.ext import commands
import random

class Maintain(commands.Cog):
    def __init__(self, bot, anilist_api, emojis, config):
        self.bot = bot
        self.anilist_api = anilist_api
        self.emojis = emojis

    @commands.command()
    async def add(self, ctx, anilist_url):
        """ provide anilist url to add to PTW list """

        # add to the existing anilist
        result = self.anilist_api.add(anilist_url)

        # build emojis
        positive_emoji = self.bot.get_emoji(random.choice(self.emojis['positive']))
        negative_emoji = self.bot.get_emoji(random.choice(self.emojis['negative']))

        # respond to the user depending on the attempt
        if result:
            usr_msg = "かしこまりました、ご主人様。"
            usr_msg += "\nI have successfully updated anilist!"
            await ctx.send(usr_msg)
            await ctx.send(positive_emoji)
        else:
            usr_msg = "申し訳ありません、ご主人様！！"
            usr_msg += "\nI was unable to process your command!"
            await ctx.send(usr_msg)
            await ctx.send(negative_emoji)

    @commands.command()
    async def update(self, ctx, anilist_url, progress):
        """ provide an anilist url and episode progress (e.g. +2, -4, 7) """

        # update anilist with the episode count
        result = self.anilist_api.update(anilist_url, progress=progress)
        title = self.anilist_api.get_title(anilist_url)

        # build emojis
        positive_emoji = self.bot.get_emoji(random.choice(self.emojis['positive']))
        negative_emoji = self.bot.get_emoji(random.choice(self.emojis['negative']))

        # respond to the user depending on the attempt
        if result:
            previous_progress = result[0]
            current_progress = result[1]
            usr_msg = "かしこまりました、ご主人様。"
            usr_msg += "\nI have successfully updated anilist!"
            usr_msg += f"\n{title}: {previous_progress} --> {current_progress}"
            await ctx.send(usr_msg)
            await ctx.send(positive_emoji)
        else:
            usr_msg = "申し訳ありません、ご主人様！！"
            usr_msg += "\nI was unable to process your command!"
            await ctx.send(usr_msg)
            await ctx.send(negative_emoji)

    @commands.command()
    async def rate(self, ctx, anilist_url, score):
        """ provide an anilist url and a score to rate an anime """

        # update anilist with the rating
        result = self.anilist_api.rate(anilist_url, score=score)
        title = self.anilist_api.get_title(anilist_url)

        # build emojis
        positive_emoji = self.bot.get_emoji(random.choice(self.emojis['positive']))
        negative_emoji = self.bot.get_emoji(random.choice(self.emojis['negative']))

        # respond to the user depending on the attempt
        if result:
            usr_msg = "かしこまりました、ご主人様。"
            usr_msg += "\nI have successfully updated anilist!"
            await ctx.send(usr_msg)
            await ctx.send(positive_emoji)
        else:
            usr_msg = "申し訳ありません、ご主人様！！"
            usr_msg += "\nI was unable to process your command!"
            await ctx.send(usr_msg)
            await ctx.send(negative_emoji)
