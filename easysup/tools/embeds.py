import discord
from datetime import datetime, timezone
from easysup.config import constants

# Create an embed message with the twitch user information
def EmbedNotification(streamer_data, user_data):
    user_login    = streamer_data['user_login']
    twitch_url    = constants.TWITCH_URL.format(user_login)
    capture_url   = streamer_data['thumbnail_url'].format(width=960, height=540)
    game_name     = streamer_data['game_name']
    viewer_count  = streamer_data.get('viewer_count', 0)

    display_name  = user_data['display_name']
    avatar_url    = user_data['profile_image_url']

    stream_title = str(streamer_data['title']).replace("||", "| |")

    embed = discord.Embed(title=stream_title, url=twitch_url, color=0x6441a5)
    embed.add_field(name=constants.INFO_GAME, value=game_name)
    embed.add_field(name=constants.INFO_VIEWERS, value=viewer_count)
    embed.set_image(url=capture_url)
    embed.set_author(name=display_name,  icon_url=avatar_url, url=twitch_url)
    embed.timestamp = datetime.utcnow()
    embed.set_footer(text='EasySup')
    return embed

def EmbedUserData(user_data):
    user_login = user_data['login']
    twitch_url = constants.TWITCH_URL.format(user_login)

    total_followers = user_data['followers']

    d = datetime.fromisoformat('2020-01-06T00:00:00.000Z'[:-1]).astimezone(timezone.utc)
    created_at = d.strftime('%Y-%m-%d')

    title = "{0} en Twitch".format(user_data['display_name'])

    embed = discord.Embed(title=title, 
                          url=twitch_url, color=0x6441a5,
                          description=user_data['description'])
    embed.set_thumbnail(url=user_data["profile_image_url"])
    embed.add_field(name=constants.INFO_CREATED_AT, value=created_at)
    embed.add_field(name=constants.INFO_FOLLOWERS,  value=total_followers)
    #embed.set_author(name="Twitch User",  icon_url=user_data["profile_image_url"], url=twitch_url)

    return embed
