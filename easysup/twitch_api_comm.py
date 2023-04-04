import os
import requests
from urllib.parse import urlparse

# Authentication with Twitch API.
client_id = os.environ['TWICTH_CLIENT_ID']
client_secret = os.environ['TWITCH_CLIENT_SECRET']
body = {
 'client_id': client_id,
 'client_secret': client_secret,
 "grant_type": 'client_credentials'
}
r = requests.post('https://id.twitch.tv/oauth2/token', body)
keys = r.json()
headers = {
 'Client-ID': client_id,
 'Authorization': 'Bearer ' + keys['access_token']
}


# Returns true if online, false if not.
def GetStreamData(streamers: list):
	try:
		query_params = '&user_login='.join(streamers)

		response = requests.get(
		 f'https://api.twitch.tv/helix/streams?user_login={query_params}',
		 headers=headers)

		if response.status_code != 200:
			return []

		stream_data = response.json().get('data', [])

		stream_dict = {
		 stream['user_login']: {
		  'user_login': stream['user_login'],
		  'user_name': stream['user_name'],
		  'game_name': stream['game_name'],
		  'thumbnail_url': stream['thumbnail_url'],
		  'title': stream['title'],
		  'viewer_count': stream['viewer_count'],
		  'tags': stream['tags'],
		  'is_live': True
		 }
		 for stream in stream_data
		}

		result = []
		for streamer in streamers:
			if streamer in stream_dict:
				result.append(stream_dict[streamer])
			else:
				result.append({
				 'user_login': streamer,
				 'user_name': None,
				 'game_name': None,
				 'thumbnail_url': None,
				 'title': None,
				 'viewer_count': None,
				 'tags': None,
				 'is_live': False
				})

		return result

	except requests.exceptions.RequestException:
		return []


# Returns data of user.
def GetUserData(user_login):
	try:
		response = requests.get(
		 f'https://api.twitch.tv/helix/users?login={user_login}', headers=headers)

		if response.status_code != 200:
			return []

		user_data = response.json().get('data', [])

		if len(user_data) == 1:
			return user_data[0]

	except requests.exceptions.RequestException:
		return []


# Get total followers according to user
def GetTotalFollowers(broadcaster_id) -> int:
	try:
		response = requests.get(
		 f"https://api.twitch.tv/helix/channels/followers?broadcaster_id={broadcaster_id}&first=1",
		 headers=headers)

		if response.status_code != 200:
			return 0

		total_followers = response.json().get('total', 0)
		return total_followers
	except requests.exceptions.RequestException:
		return 0


# Returns data of clips.
def getDataClip(url):
	try:
		clip_id = urlparse(url).path.lstrip('/')
		response = requests.get(f"https://api.twitch.tv/helix/clips?id={clip_id}",
		                        headers=headers)

		if response.status_code != 200:
			return None

		clip_data = response.json().get('data', [])
		#return clip_data[0] if len(clip_data) == 1 else clip_data
		return clip_data
	except requests.exceptions.RequestException:
		return None
