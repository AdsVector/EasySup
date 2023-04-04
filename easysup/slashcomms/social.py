import discord 
from discord import app_commands
from discord.ui import View, Button

from typing import Optional
from easysup.manager.LinksManager import LinksManager
from easysup.config import config
from easysup.linkutils import identify_emoji_url, is_valid_url

class Dropdown(discord.ui.Select):
    def __init__(self, options, min:int = 1, max:int = 1):
        super().__init__(placeholder='Select an option', options=options, min_values=min, max_values=max)

    async def callback(self, interaction: discord.Interaction):
        try:
            self.view.selected = True
    
            if self.manager.delete_elements(str(self.user.id), self.values, 'socialName'):
                links = ', '.join(self.values)
                await interaction.response.edit_message(content=f'{links} se han eliminado', view=None)
            else:
                await interaction.response.edit_message(content=f'Hubo un error al eliminar datos', view=None)
        except Exception as e:
            print(f"CustomMenu <> An error occurred: {e}")

class DropdownView(discord.ui.View):
    def __init__(self, timeout=1):
        self.selected = False
        super().__init__(timeout=timeout)

    async def on_timeout(self):
        try:
            self.clear_items()
            if not self.selected:  # Verificar si se ha seleccionado un valor
                await self.message.edit(content=config.TIMEOUT_MESSAGE, view=None)
        except Exception as e:
            print(f"TimeOut <> An error occurred: {e}")

class Links(app_commands.Group):
    def __init__(self) -> None:
        super().__init__(name="links", description="Añadir, eliminar y mostrar tu enlances a redes sociales")
        self.manager = LinksManager(config.SOCIALNETWORKS_PATH)

    @app_commands.command(name="add", description="Añade nuevos vínculos de a tu perfil.")
    @app_commands.describe(user="Usuario a trabajar", name="Nombre de la página", url="URL de vuestra página.")
    async def add_link(self, interaction: discord.Interaction, user: Optional[discord.User], name: str, url:str):
        try:
            if user and not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("No puedes modificar los vínculos de otros usuarios.", ephemeral=True)
                return
        
            user  = user or interaction.user
            if self.manager.count([str(user.id)]) == 5:
                await interaction.response.send_message("Lo sentimos, ya no puedes añadir más vínculos.\n Intenta después de eliminar uno anterior.")
                return
            
            if not is_valid_url(url):
                await interaction.response.send_message("⛔ Introduce una URL válida.")
                return

            socialData = {
                "socialName" : name,
                "socialUrl"  : url 
            }

            saved = self.manager.add_element(str(user.id), socialData)

            if(saved and user == interaction.user):
                await interaction.response.send_message(f"Has agregado un nuevo vínculo: {name}.")
            else:
                await interaction.response.send_message(f"{name} agregado para {user.mention}.")
        except Exception as e:
            print(f"Add Social <> An error occurred: {e}")

    @app_commands.command(name="remove", description="Elimina tus vínculos almacenados.")
    @app_commands.describe(user="Usuario a trabajar")
    async def remove_link(self, interaction: discord.Interaction, user: Optional[discord.User]):
        try:            
            if user and not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("No puedes crear enlaces personalizado.", ephemeral=True)
                return

            user = user or interaction.user
            networks =  self.manager.data[str(user.id)]
            if not networks:
                await interaction.response.send_message(f"No existen vínculos almacenados para {user.mention}.", ephemeral=True)
                return

            options = []
            for network in networks:
                option = discord.SelectOption(
                    label=network["socialName"], 
                    description=network["socialUrl"])
                options.append(option)

            menu = Dropdown(options=options, max=len(options))
            menu.user    = user
            menu.manager = self.manager
           
            view = DropdownView(timeout=30)
            view.add_item(menu)
            view.message = await interaction.response.send_message(f'**Eliminar Vínculo/s** para {user.mention}', view=view, ephemeral=True)              
        except Exception as e:
            print(f"Remove Social <> An error occurred: {e}")

    @app_commands.command(name="show_all", description="Muestra todos los enlaces de un usuario.")
    @app_commands.describe(user="Mostrarás la redes de este usuario.", message="Añade un mensaje para mostrar.")
    async def show_all(self, interaction: discord.Interaction, user: Optional[discord.User], message : Optional[str] = ""):
        try:            
            user = user or interaction.user
            networks = self.manager.data[str(user.id)]

            v = View()
            for network in networks:
                title = network["socialName"]
                url   = network["socialUrl"]
                emoji = identify_emoji_url(url=url)
                btn = Button(label = title, url   = url, emoji = emoji)
                v.add_item(btn)

            message += f'\n\n Mostrando la redes sociales de {user.mention}'
            
            await interaction.response.send_message(content=message, view=v)    
                  
        except Exception as e:
            print(f"Remove Social <> An error occurred: {e}")

    async def links_autocomplete(self, interaction: discord.Interaction, 
                            current: str) -> list[app_commands.Choice[str]]:
        networks = self.manager.data[str(interaction.user.id)]
        return [
            app_commands.Choice(name=link["socialName"], value=link["socialName"])
            for link in networks if current.lower() in str(link['socialName']).lower()
        ]


    @app_commands.command(name="share-link", description="Comparte una de tus redes con un mensaje")
    @app_commands.autocomplete(link=links_autocomplete)    
    async def share_link(self, interaction: discord.Interaction, link : str,  message : Optional[str] = ""):
        title, url = self.manager.search_link(str(interaction.user.id), link)
        emoji = identify_emoji_url(url=url)
        btn = Button(label = title, url   = url, emoji = emoji)

        v = View()
        v.add_item(btn)
            
        if message:
            message = f"**{interaction.user}**: " + message 

        await interaction.response.send_message(content=message, view=v)              

    @app_commands.command(name="share", description="Comparte una de tus redes con un mensaje")
    async def show_link(self, interaction: discord.Interaction, name_link : str, link: str,  message : Optional[str] = ""):
        try:
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("No puedes crear enlaces personalizado.", ephemeral=True)
                return
            
            emoji = identify_emoji_url(url=link)
            btn = Button(label = name_link, url = link, emoji = emoji)

            v = View()
            v.add_item(btn)
            
            if message:
                message = f"**{interaction.user}**: " + message 

            await interaction.response.send_message(content=message, view=v) 
        except Exception as e:
            print(f"Social Media <> An error occurred: {e}")
   
async def setup(bot):
    bot.tree.add_command(Links())