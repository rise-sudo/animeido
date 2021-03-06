""" auth token
related to anilist oauth mechanism
generates a token based off the auth code generated from the auth_code utility script """

import requests
import dotenv

# set up environmental variables
config = dotenv.dotenv_values('.env')

# auth code that was generated by the auth_code utility script
auth_code = config['AUTH_CODE']

# client id that is assigned to the animeido anilist api client
client_id = config['CLIENT_ID']

# client secret that is assigned to the animeido anilist api client
client_secret = config['CLIENT_SECRET']

# useful redirect uri provided by anilist in case there is no html schema being used
redirect_uri = config['REDIRECT_URI']

# base url for the api call
url = 'https://anilist.co/api/v2/oauth/token'

# headers
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

# json
json = {
    'grant_type': 'authorization_code',
    'client_id': f'{client_id}',
    'client_secret': f'{client_secret}',
    'redirect_uri': f'{redirect_uri}', 
    'code': f'{auth_code}',
}

# send the post response to generate the token
response = requests.post(url, json=json, headers=headers)

# store token response
token_response = response.json()

# print the token info to the screen
print(f"token_type: {token_response['token_type']}")
print(f"expires_in: {token_response['expires_in']}")
print(f"access_token: {token_response['access_token']}")
print(f"refresh_token: {token_response['refresh_token']}")