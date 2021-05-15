""" auth code
related to anilist oauth mechanism
authorizes animeido bot to access the user's anilist profile """

import webbrowser
from dotenv import dotenv_values

# set up environmental variables
config = dotenv_values('.env')

# client id that is assigned to the spoopy weeb bot api client
client_id = config['CLIENT_ID']

# useful redirect uri provided by anilist in case there is no html schema being used
redirect_uri = config['REDIRECT_URI']

# base url for the api call
base_url = 'https://anilist.co/api/v2/oauth/authorize'

# build the full url accordingly
url = f'{base_url}?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code'

# ask the user to sign into their anilist account on their browser
usr_msg = "Please sign into your anilist account via your web browser (press any key to continue)"
input(usr_msg)

# open the url in the browser
webbrowser.open(url)