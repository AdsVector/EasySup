from easysup.config.constants import TWITCH_URL

def get_role(guild, role_id):
    if role_id is not None:
        role = guild.get_role(role_id)
        if role is None:
            print(f"Role with ID {role_id} not found in guild {guild.name}")
        return role
    return None

def format_message(msg: str, data):
    display_name = data.get('user_name', 'Unknown')
    game_name    = data.get('game_name', 'Unknown')
    twitch_url   = TWITCH_URL.format(data.get('login', ''))
    
    message = msg.format(
                    display_name=display_name, 
                    game_name=game_name, 
                    twitch_url=twitch_url)
    
    return message