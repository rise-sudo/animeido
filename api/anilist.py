""" anilist
an api wrapper library for the anilist APIv2 """

import requests
import dotenv

class AniList:

    def __init__(self):
        # set up environmental variables
        config = dotenv.dotenv_values('.env')

        # anilist user to modify
        self.anilist_user = config['ANILIST_USER']

        # bearer token for privileged operations
        self.bearer_token = config['BEARER_TOKEN']

    def search(self, search_term, media_type='ANIME'):
        """ search
        enables search of anilist catalogue
        default searches through anime but set up to be able to search
        through every single catalogue if needed in the future """

        # initialize anilist url list
        anilist_urls = []

        # base graphql api url
        url = 'https://graphql.anilist.co'

        # build query string
        query = '''
            query ($id: Int, $page: Int, $perPage: Int, $search: String, $type: MediaType) {
                Page (page: $page, perPage: $perPage) {
                    pageInfo {
                        total
                        currentPage
                        lastPage
                        hasNextPage
                        perPage
                    }
                    media (id: $id, search: $search, type: $type) {
                        id
                        title {
                            romaji
                            native
                        }
                    }
                }
            }
        '''

        # build variables
        variables = {
            'search': search_term,
            'type': media_type,
            'page': 1,
            'perPage': 5,
        }

        # send api call 
        response = requests.post(url, json={'query': query, 'variables': variables})

        # kill method early assuming api call failed
        if response.status_code != 200:
            return anilist_urls

        # set up data which contains the anilist result
        data = response.json()['data']['Page']

        # build url list
        for anime_entry in data['media']:
            title = anime_entry['title']['romaji']
            anilist_url = f"https://anilist.co/{media_type.lower()}/{anime_entry['id']}/"
            anilist_urls.append([title, anilist_url])

        # return anime urls
        return anilist_urls

    def get_title(self, anilist_url):
        """ get url
        enables search of anilist catalogue via url
        and returns the title of the anilist entry
        will be used internally by the bot """

        # initialize media id based off url
        media_id = 0
        if 'anilist' in anilist_url:
            try:
                media_id = int(anilist_url.split('anilist')[-1].split('/')[2])
            except ValueError:
                return False
        else:
            return False

        # base graphql api url
        url = 'https://graphql.anilist.co'

        # build query string
        query = '''
            query ($id: Int) {
                Media (id: $id) {
                    id
                    title {
                        romaji
                        native
                    }
                }
            }
        '''

        # build variables
        variables = {
            'id': media_id,
        }

        # send api call 
        response = requests.post(url, json={'query': query, 'variables': variables})

        # kill method early assuming api call failed
        if response.status_code != 200:
            return False

        # capture the title of the search media
        title = response.json()['data']['Media']['title']['romaji']

        # return title
        return title

    def add(self, anilist_url, media_status='PLANNING'):
        """ add
        enables adding anilist media to planning to watch list by default
        will also add capability to add directly to other states as well """

        # initialize media id based off url
        media_id = 0
        if 'anilist' in anilist_url:
            try:
                media_id = int(anilist_url.split('anilist')[-1].split('/')[2])
            except ValueError:
                return False
        else:
            return False

        # base graphql api url
        url = 'https://graphql.anilist.co'

        # build headers
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        # build query string
        query = '''
            mutation ($mediaId: Int, $status: MediaListStatus) {
                SaveMediaListEntry (mediaId: $mediaId, status: $status) {
                    id
                    status
                }
            }
        '''

        # build variables
        variables = {
            'mediaId': media_id,
            'status': media_status,
        }

        # send api call 
        response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

        # inform whether call was successful or not
        if response.status_code != 200:
            return False
        else:
            return True

    def get_current_progress(self, anilist_url):
        """ get current progress
        get the current progress of the media specified """

        # initialize progress
        progress = 0

        # initialize media id based off url
        media_id = 0
        if 'anilist' in anilist_url:
            try:
                media_id = int(anilist_url.split('anilist')[-1].split('/')[2])
            except ValueError:
                return progress
        else:
            return progress

        # base graphql api url
        url = 'https://graphql.anilist.co'

        # build query string
        query = '''
            query ($mediaId: Int, $userName: String) {
                MediaList (mediaId: $mediaId, userName: $userName) {
                    id
                    progress
                }
            }
        '''

        # build variables
        variables = {
            'mediaId': media_id,
            'userName': self.anilist_user,
        }

        # send api call 
        response = requests.post(url, json={'query': query, 'variables': variables})

        # kill method early assuming api call failed
        if response.status_code != 200:
            return progress

        # grab the current progress on the media entry
        progress = response.json()['data']['MediaList']['progress']

        return progress

    def _get_max_episodes(self, media_id):
        """ get max episodes
        gets the available max episodes of the media specified """

        # initialize episodes
        episodes = 10000

        # base graphql api url
        url = 'https://graphql.anilist.co'

        # build query string
        query = '''
            query ($id: Int) {
                Media (id: $id) {
                    id
                    episodes
                }
            }
        ''' 

        # build variables
        variables = {
            'id': media_id,
        }

        # send api call 
        response = requests.post(url, json={'query': query, 'variables': variables})

        # kill method early assuming api call failed
        if response.status_code != 200:
            return episodes

        # grab the episode count from the data
        episodes = response.json()['data']['Media']['episodes']

        return episodes

    def update(self, anilist_url, media_status='CURRENT', progress=0):
        """ update
        enables updating anilist media to whatever state we want """

        # initialize media id based off url
        media_id = 0
        if 'anilist' in anilist_url:
            try:
                media_id = int(anilist_url.split('anilist')[-1].split('/')[2])
            except ValueError:
                return False
        else:
            return False

        # track previous progress
        previous_progress = self.get_current_progress(anilist_url)

        # check if progress is additive or static
        try:
            # convert progress to string temporarily
            progress = str(progress)
            max_episodes = self._get_max_episodes(media_id)

            # check if user provided additive values
            if '+' in progress or '-' in progress:
                progress = previous_progress + int(progress)

                # verify value did not go below zero
                if int(progress) < 0:
                    progress = 0
                # verify value did not go above max episodes
                elif int(progress) >= max_episodes:
                    progress = max_episodes
                    media_status = 'COMPLETED'

            # otherwise use the progress as is
            else:
                progress = int(progress)
                # verify value did not go above max episodes
                if progress >= max_episodes:
                    progress = max_episodes
                    media_status = 'COMPLETED'
                # use current progress if user provided no value besides 0
                elif progress == 0:
                    progress = previous_progress

        # exception in case of value error
        except ValueError:
            return False

        # base graphql api url
        url = 'https://graphql.anilist.co'

        # build headers
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        # build query string
        query = '''
            mutation ($mediaId: Int, $status: MediaListStatus, $progress: Int) {
                SaveMediaListEntry (mediaId: $mediaId, status: $status, progress: $progress) {
                    id
                    status
                    progress
                }
            }
        '''

        # build variables
        variables = {
            'mediaId': media_id,
            'status': media_status,
            'progress': progress,
        }

        # send api call 
        response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

        # inform whether call was successful or not
        if response.status_code != 200:
            return False
        else:
            current_progress = self.get_current_progress(anilist_url)
            return [previous_progress, current_progress]

    def rate(self, anilist_url, score=0, media_status='COMPLETED'):
        """ rate
        enables updating the rating for the media entry """

        # initialize media id based off url
        media_id = 0
        if 'anilist' in anilist_url:
            try:
                media_id = int(anilist_url.split('anilist')[-1].split('/')[2])
            except ValueError:
                return False
        else:
            return False

        # base graphql api url
        url = 'https://graphql.anilist.co'

        # build headers
        headers = {
            'Authorization': f'Bearer {self.bearer_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }

        # build query string
        query = '''
            mutation ($mediaId: Int, $status: MediaListStatus, $score: Float) {
                SaveMediaListEntry (mediaId: $mediaId, status: $status, score: $score) {
                    id
                    status
                    score
                }
            }
        '''

        # build variables
        variables = {
            'mediaId': media_id,
            'status': media_status,
            'score': score,
        }

        # send api call 
        response = requests.post(url, headers=headers, json={'query': query, 'variables': variables})

        # inform whether call was successful or not
        if response.status_code != 200:
            return False
        else:
            return True