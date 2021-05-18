""" provide
cog that handles all information related tasks
such as providing the user with help or information """

from discord.ext import commands
import discord

class Provide(commands.Cog):
    def __init__(self, bot, anilist_api, emojis, config):
        self.bot = bot
        self.anilist_api = anilist_api
        self.emojis = emojis
        self.icon_url = config['ICON_URL']
        self.anilist_user = config['ANILIST_USER']

    @commands.Cog.listener()
    async def on_ready(self):
        """ on ready
        generates a message once the bot has successfully logged into discord """

        # print to the console screen
        print(f'Logged in as {self.bot.user.name} with id of {self.bot.user.id}.')
        print('------')

    @commands.command()
    async def search(self, ctx, *search_term: str):
        """ search with any term or terms """

        # search via the anilist api and get the url results
        anilist_urls = self.anilist_api.search(' '.join(search_term))

        # set up embed
        embed = discord.Embed(
            title="AniList Search",
            color=0xaaa9ad,
            description=f"Found {len(anilist_urls)} matches!"
        )
        embed.set_author(
            name="アニメイド", 
            icon_url=self.icon_url, 
            url=f"https://anilist.co/user/{self.anilist_user}/"
        )
        embed.set_thumbnail(url=self.icon_url)

        # iterate through the urls and send to user
        for anilist_url in anilist_urls:
            title = anilist_url[0]
            url = anilist_url[1]
            embed.add_field(name=title, value=url, inline=False)
            
        await ctx.send(embed=embed)
