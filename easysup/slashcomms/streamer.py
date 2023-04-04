import discord 
from discord import app_commands
from discord.ext import tasks, commands
from discord.ext.commands import has_permissions, MissingPermissions

import random
from typing import Optional
from easysup.config import config
from easysup.utils import format_message
from easysup.twitch_api_comm import GetStreamData, GetUserData, GetTotalFollowers
from easysup.tools.embeds import EmbedNotification, EmbedUserData
from easysup.manager.JsonFileManager import JSON_Manager

class Streamer(app_commands.Group):
    def __init__(self) -> None:
        super().__init__(name="streamer", description="Puedes añadir o eliminar streamer en tu canal.")
        self.manager = JSON_Manager(config.STREAMERS_PATH)

    @app_commands.command(name="add", description="Añade un nuevo streamer para recibir notificaciones.")
    @app_commands.describe(twitch_name="Nombre del streamer. Solo Twitch!", 
                           user="Usuario a cual se le dará rol.", 
                           message="Puedes mostrar un mensaje personalizado")
    @app_commands.checks.has_permissions(administrator=True)
    async def add_streamer(self, interaction: discord.Interaction, twitch_name:str, user: Optional[discord.User], message: Optional[str]):
        try: 
            twitch_name = twitch_name.lower()
            guild_id    = interaction.guild_id

            user_data = GetUserData(twitch_name)
            if not user_data:
                await interaction.response.send_message(f"El usuario **{twitch_name}** no existe.")
                return

            # Verificar si el usuario ya existe en la lista de streamers
            if twitch_name in self.manager.data[str(guild_id)].get('streamers', []):
                await interaction.response.send_message("El streamer ya existe en la lista.")
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
            await interaction.response.send_message("El streamer se ha añadido correctamente.", embed=embed)
        except Exception as e:
             print(f"An error occurred: {e}")  

    @add_streamer.error
    async def add_streamer_error(interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("No tienes permisos para añadir un streamer.", ephemeral=True)
        else: raise error

    @app_commands.command(name="remove", description="Elimina un streamer, está acción no es reversible.")
    @app_commands.describe(twitch_name="Nombre del streamer. Solo Twitch!")
    @app_commands.checks.has_permissions(administrator=True)
    async def remove_streamer(self, interaction: discord.Interaction, twitch_name:str):
        try:
            guild_id  = interaction.guild_id
    
            if self.manager.delete_elements([str(guild_id), 'streamers'], [twitch_name]):
                await interaction.response.send_message("El streamer se ha eliminado correctamente")
            else:
                await interaction.response.send_message("Hubo un problema a eliminar.")
        except Exception as e:
            print(f"An error occurred: {e}")  
    
    @remove_streamer.autocomplete('twitch_name')
    async def streamer_autocomplete(self, interaction: discord.Interaction, 
                            current: str) -> list[app_commands.Choice[str]]:
        streamers = self.manager.data[str(interaction.guild_id)]['streamers'].keys()
        return [
            app_commands.Choice(name=streamer, value=streamer)
            for streamer in streamers if current.lower() in str(streamer).lower()
        ]

    @remove_streamer.error
    async def remove_streamer_error(interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message("No tienes permisos para eliminar un streamer.", ephemeral=True)
        else: raise error

    @app_commands.command(name="is_live", description="Necesitas saber si un streamer esta en vivo.")
    async def twitch_user(self,  interaction: discord.Interaction, username:str):
        try:
            username = username.lower()

            user_data = GetUserData(username)
            
            if not user_data:
                await interaction.response.send_message(f"El usuario **{username}** no existe.")
                return

            streamers = []
            streamers.append(username)
            streamer_data = GetStreamData(streamers)[0]
            url_twitch = config.TWITCH_URL.format(user_data['login'])
            
            if streamer_data['is_live'] is False:
                user_data["followers"] = GetTotalFollowers(user_data['id'])
                msg = "El usuario no está actualmente en vivo..! **No te olvides de seguirlo.**"
                embed = EmbedUserData(user_data)
                view = discord.ui.View()
                view.add_item(discord.ui.Button(
                                        label="Visit Profile",
                                        style=discord.ButtonStyle.link,
                                        url=url_twitch))
                await interaction.response.send_message(embed=embed, content=msg,  view=view)
                return
            
            msg     = config.DEFAULT_MSG[random.randint(0, 5)]  
            message = format_message(msg=msg, data=streamer_data)
            embed   = EmbedNotification(streamer_data, user_data)
            view    = discord.ui.View() 
            view.add_item(discord.ui.Button(
                                    label=config.WATCH_BUTTON,
                                    style=discord.ButtonStyle.link,
                                    url=url_twitch))
            await interaction.response.send_message(embed=embed, content=message,  view=view)
        except Exception as e:
            print(f"An error occurred: {e}")  
    




async def setup(bot):
    bot.tree.add_command(Streamer())