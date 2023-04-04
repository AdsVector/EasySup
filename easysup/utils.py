from easysup.config import config

def format_message(msg: str, data):
    display_name = data.get('user_name', 'Unknown')
    game_name    = data.get('game_name', 'Unknown')
    twitch_url   = config.TWITCH_URL.format(data.get('login', ''))
    
    message = msg.format(
                    display_name=display_name, 
                    game_name=game_name, 
                    twitch_url=twitch_url)
    
    return message