import discord 
from discord import app_commands
from discord.ext import tasks, commands
from discord.ext.commands import has_permissions, MissingPermissions

from easysup.json_managers.JsonFileManager import JSON_Manager
from easysup.config.constants import STREAMERS_PATH

class Setup(app_commands.Group):
    def __init__(self) -> None:
        super().__init__(name="setup", description="Puedes configurar el canal y roles para las notificaciones.")
        self.manager = JSON_Manager(STREAMERS_PATH)

    @app_commands.command(name="channel", description="Establezca el canal donde se enviarán las notificaciones.")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_channel(self, interaction: discord.Interaction, channel : discord.TextChannel):
        try:
            guild_id = interaction.guild_id
            if self.manager.update_element([str(guild_id), 'settings'], 'channel', channel.id):
                await interaction.response.send_message(f"Ahora el nuevo canal de notificaciones será {channel.mention}")
            else:
                await interaction.response.send_message(f"¡Hubo problemas! No se pudo cambiar el canal.")
        except Exception as e:
            print(f"Set-Channel <> An error occurred: {e}")

    @app_commands.command(name='role-live',  description="Establezca el rol que obtendrán los usuarios en vivo.")
    @app_commands.checks.has_permissions(administrator=True)
    async def role_streamer(self, interaction: discord.Interaction, role : discord.Role):
        try:
            guild_id = interaction.guild_id
            if self.manager.update_element([str(guild_id)], 'channel', role.id):
                await interaction.response.send_message(f"Ahora el nuevo rol de streamers será {role.mention}")
            else:
                await interaction.response.send_message(f"¡Hubo problemas! No se pudo cambiar el canal.")
        except Exception as e:
            print(f"Set-Channel <> An error occurred: {e}")

    @app_commands.command(name='role-receive', description="Establezca el rol para mencionar a los usuarios en las notificaciones.")
    @app_commands.checks.has_permissions(administrator=True)
    async def role_receive(self, interaction: discord.Interaction, role : discord.Role):
        try:
            guild_id = interaction.guild_id
            if self.manager.update_element([str(guild_id)], 'channel', role.id):
                await interaction.response.send_message(f"Ahora el nuevo rol para notificar será {role.mention}")
            else:
                await interaction.response.send_message(f"¡Hubo problemas! No se pudo cambiar el canal.")
        except Exception as e:
            print(f"Set-Channel <> An error occurred: {e}")

async def setup(bot):
    bot.tree.add_command(Setup())