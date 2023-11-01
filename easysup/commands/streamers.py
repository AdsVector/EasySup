import discord 
from discord.ext import tasks, commands

from typing import Optional
from ..config.constants import STREAMERS_PATH
from easysup.twitch_api_comm import GetStreamData, GetUserData, GetTotalFollowers
from easysup.tools.embeds import EmbedNotification, EmbedUserData
from easysup.json_managers.JsonFileManager import JSON_Manager

class Streamers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.manager = JSON_Manager(STREAMERS_PATH)
       

    @commands.command(name='add', aliases=['add-streamer'], pass_context=True)
    async def add_notify(self, ctx, twitch_name:str, user: Optional[discord.User], *, message: Optional[str]):
        try: 
            twitch_name = twitch_name.lower()
            guild_id = ctx.message.guild.id

            user_data = GetUserData(twitch_name)
            if not user_data:
                await ctx.send(f"El usuario **{twitch_name}** no existe.")
                return

            # Verificar si el usuario ya existe en la lista de streamers
            if twitch_name in self.manager.get_value([str(guild_id), 'streamers'], []):
                await ctx.send("El streamer ya existe en la lista.")
                return

            data = {
                "user_id": (user.id if user else ""), 
                "message": message, 
                "sent": False
            }

            self.manager.add_element([str(guild_id), 'streamers', twitch_name], data)

            user_data = GetUserData(twitch_name)
            user_data["followers"] = GetTotalFollowers(user_data['id'])
            embed = EmbedUserData(user_data)
            await ctx.send("El streamer se ha añadido correctamente.", embed=embed)
        except Exception as e:
             print(f"An error occurred: {e}")  

    @commands.command(name='del', aliases=['remove-streamer', 'del-streamer'])
    async def remove_notify(self, ctx, *twitch_names:str):
        try:
            guild_id  = ctx.message.guild.id
            streamers = self.manager.get_value([str(guild_id), 'streamers'], {})

            for name in twitch_names:
                if not (name in streamers):   
                    await ctx.send(f"El **{name}** no se encuentra en la lista.")
                    return

            if self.manager.delete_elements([str(guild_id), 'streamers'], twitch_names):
                await ctx.send("El streamer se ha eliminado correctamente")
            else:
                await ctx.send("Hubo un problema a eliminar.")
        except Exception as e:
            print(f"An error occurred: {e}")  
            

async def setup(bot):
    await bot.add_cog(Streamers(bot))
