import os


TW_CLIENT_ID = "t29lvsfrateaygfdt3gm6s3vbi8h3w"
TW_CLIENT_SECRET = "b1igkh59vm2r1g0mvupnvyzb0qmjnw"


#BOT_TOKEN = os.environ['DISCORD_TOKEN']
BOT_TOKEN = "OTU0MzQ3NTgyOTA0MjA1MzYz.GjAvob.rVS5jOa2t0gJLcEzz78MwR7g1Xw85utPXOFFU0"
BOT_PREFIX = "$"


STREAMERS_PATH = "easysup/config/streamers.json"
SENTS_PATH = "easysup/config/sents.json"
SOCIALNETWORKS_PATH = "easysup/config/Networks.json"


WAITING_MESSAGE = "Waiting..."
CHECKING_LIVE_USERS = "Sending Notifications..."

TWITCH_URL = "https://twitch.tv/{0}"

INFO_GAME = "Actividad/Juego"
INFO_VIEWERS = "Viewers"
INFO_CREATED_AT = "Created At:"
INFO_FOLLOWERS = "Followers:"
TIMEOUT_MESSAGE = "Se ha agotado el tiempo de espera."
WATCH_BUTTON = "Watch Stream"

DEFAULT_MSG = [
 "¡Ey! **{display_name}** está transmitiendo **{game_name}** en vivo.\n ¡No te lo pierdas en {twitch_url} !",
 "¡Es hora de relajarse y ver un buen stream! Únete a nosotros en nuestro canal de Twitch mientras jugamos **{game_name}** y pasamos un buen rato.\n {twitch_url}",
 "¡Atención, fanáticos de **{game_name}**!\nEstamos transmitiendo en vivo ahora mismo en nuestro canal de Twitch. ¡Ven y mira lo que estamos haciendo!",
 "¡Atención! ¡Estamos transmitiendo en vivo! ¡Únete a nosotros en nuestro canal de Twitch para ver la acción en tiempo real!",
 "¡Te invito a unirte al emocionante stream de **{display_name}**! Únete a nosotros en **{game_name}**. ¡No te lo pierdas!"
]

EMOJIS = {
    "DISCORD" : "<:discord:1091906496784244837>",
	"FACEBOOK" : "<:facebook:1091906499351167097>",
	"GITHUB" : "<:github:1091913551389667440>",
	"INSTAGRAM" : "<:instagram:1092017184957538335>",
	"SOUNCLOUD" : "<:soundcloud:1091906723238907915>",
	"SPOTIFY" : "<:spotify:1091745692004917370>",
	"TIKTOK" : "<:tiktok:1091748713015279637>",
	"TWITCH" : "<:twitch:1091747584349061291>",
	"TWITTER" : "<:twitter:1091747586291011625>",
	"YOUTUBE" : "<:youtube:1091748715020173462>",
}