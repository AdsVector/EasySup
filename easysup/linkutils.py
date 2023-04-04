
from enum import Enum
from urllib.parse import urlparse
from easysup.config.config import emojis

class Sites(Enum):
    Unknown = 0
    YouTube = 1
    Spotify = 2
    Twitter = 5
    Custom = 6
    SoundCloud = 7
    Twitch = 8
    TikTok = 9
    GitHub = 10

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def identify_url(url):
    if url is None:
        return Sites.Unknown

    if "https://www.youtube.com" in url:
        return Sites.YouTube

    if "https://open.spotify.com/artist" in url:
        return Sites.Spotify

    if "https://twitter.com/" in url:
        return Sites.Twitter

    if "soundcloud.com/" in url:
        return Sites.SoundCloud
    
    if "https://www.twitch.tv/" in url:
        return Sites.Twitch
    
    if "https://www.tiktok.com/@" in url:
        return Sites.TikTok

    if "https://github.com/" in url:
        return Sites.GitHub

    # If no match
    return Sites.Unknown

def identify_emoji_url(url):
    if url is None:
        return None

    if "https://www.youtube.com" in url:
        return emojis.YOUTUBE

    if "https://open.spotify.com/artist" in url:
        return emojis.SPOTIFY

    if "https://twitter.com/" in url:
        return emojis.TWITTER

    if "soundcloud.com/" in url:
        return emojis.SOUNCLOUD
    
    if "https://www.twitch.tv/" in url:
        return emojis.TWITCH
    
    if "https://www.tiktok.com/@" in url:
        return emojis.TIKTOK

    if "https://github.com/" in url:
        return emojis.GITHUB
    
    if "https://www.instagram.com/" in url:
        return emojis.INSTAGRAM
    
    if "https://www.facebook.com/" in url:
        return emojis.FACEBOOK

    # If no match
    return None

def split_url(url):
    # Obtiene la ruta de la URL
    path = urlparse(url).path

    # Si la URL es del tipo "https://www.youtube.com/channel/USER_ID" 
    # o "https://www.youtube.com/user/USER_NAME"
    if "/channel/" in url or "/user/" in url:
        return path.split("/")[2]

    # Si la URL es del tipo "https://www.youtube.com/@USER_NAME" o "https://www.tiktok.com/@USER_NAME"
    if "/@" in url:
        return path.split("/@")[1]
    
    if "/artist/" in url:
        return path.split("/artist/")[1]
 
    return path.split('/')[1]